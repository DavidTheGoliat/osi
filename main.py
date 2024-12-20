import cv2
import pytesseract
import sqlite3
import folium
import requests
import os
from datetime import datetime
import re

class BanknoteTracker:
    def __init__(self, db_path="db.sqlite"):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize database if it doesn't exist"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS banknote_history (
                serial_number TEXT,
                location TEXT,
                timestamp TEXT
            )
        """)
        conn.commit()
        conn.close()

    def get_location(self):
        """Get user location using IP geolocation"""
        try:
            response = requests.get("http://ip-api.com/json/", timeout=5)
            response.raise_for_status()
            data = response.json()
            return data["lat"], data["lon"], f"{data['city']}, {data['country']}"
        except Exception as e:
            print(f"Error getting location: {e}")
            return None, None, "Unknown"

    def capture_serial_number(self):
        """Capture and process the serial number via webcam"""
        print("\nWebcam Instructions:")
        print("- Hold the banknote's serial number clearly in view")
        print("- Press 's' to scan")
        print("- Press 'q' to quit")
        print("- Press 'r' to retry last scan\n")

        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not access webcam")
            return None

        last_scan = None
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Add helper text to frame
            cv2.putText(frame, "Press 's' to scan, 'q' to quit", 
                       (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

            cv2.imshow("Capture Serial Number", frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord('s'):
                # Save frame and perform OCR
                cv2.imwrite("capture.jpg", frame)
                print("\nScanning...")
                text = pytesseract.image_to_string("capture.jpg").strip()
                last_scan = text
                print(f"Detected text: {text}")
                print("Is this correct? Press 'y' to accept, 'r' to retry, 'q' to quit")
            
            elif key == ord('y') and last_scan:
                cap.release()
                cv2.destroyAllWindows()
                if os.path.exists("capture.jpg"):
                    os.remove("capture.jpg")
                return last_scan
            
            elif key == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()
        if os.path.exists("capture.jpg"):
            os.remove("capture.jpg")
        return None

    def search_serial_number(self, serial_number):
        """Search for serial number in database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT location, timestamp 
            FROM banknote_history 
            WHERE serial_number = ? 
            ORDER BY timestamp
        """, (serial_number,))
        results = cursor.fetchall()
        conn.close()
        return results

    def add_location(self, serial_number, location):
        """Add new location to database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO banknote_history VALUES (?, ?, ?)", 
                      (serial_number, location, timestamp))
        conn.commit()
        conn.close()

    def create_map(self, locations, output_file="banknote_map.html"):
        """Generate a Folium map with the banknote's journey"""
        if not locations:
            print("No locations to display on map.")
            return

        # Calculate center point of all locations
        lats, lons = zip(*[(loc[0], loc[1]) for loc in locations])
        center_lat = sum(lats) / len(lats)
        center_lon = sum(lons) / len(lons)

        # Create map
        m = folium.Map(location=[center_lat, center_lon], zoom_start=8)

        # Add markers and connect them with lines
        coordinates = []
        for idx, (lat, lon, desc) in enumerate(locations, 1):
            coordinates.append([lat, lon])
            folium.Marker(
                [lat, lon],
                popup=f"Stop {idx}: {desc}",
                icon=folium.Icon(color='red' if idx == len(locations) else 'blue')
            ).add_to(m)

        # Add line connecting all points
        if len(coordinates) > 1:
            folium.PolyLine(
                coordinates,
                weight=2,
                color='green',
                opacity=0.8
            ).add_to(m)

        m.save(output_file)
        print(f"\nMap saved as {output_file}")
        print("Open this file in a web browser to view the journey of your banknote!")

def main():
    print("\n=== Banknote Journey Tracker ===")
    tracker = BanknoteTracker()

    # Get serial number
    while True:
        choice = input("\nChoose input method:\n1. Webcam\n2. Manual entry\nChoice (1/2): ").strip()
        
        if choice == '1':
            serial_number = tracker.capture_serial_number()
        elif choice == '2':
            serial_number = input("Enter serial number: ").strip()
        else:
            print("Invalid choice. Please try again.")
            continue

        if serial_number:
            break
        print("No serial number provided. Please try again.")

    # Clean up serial number (remove spaces and special characters)
    serial_number = re.sub(r'[^A-Za-z0-9]', '', serial_number)
    print(f"\nProcessing serial number: {serial_number}")

    # Get current location
    print("\nGetting your current location...")
    lat, lon, location_desc = tracker.get_location()
    if lat is None:
        print("Could not determine your location. Exiting.")
        return

    # Add current location to database
    tracker.add_location(serial_number, location_desc)
    print(f"Added your location: {location_desc}")

    # Get history and create map
    history = tracker.search_serial_number(serial_number)
    print(f"\nFound {len(history)} previous locations for this banknote:")
    for loc, timestamp in history:
        print(f"- {loc} at {timestamp}")

    # Prepare location data for map
    locations = [(lat, lon, f"{location_desc} (Current)")] # Current location first
    for location, _ in history[:-1]:  # Exclude the just-added current location
        try:
            lat, lon = map(float, location.split(',')[:2])
            locations.append((lat, lon, location))
        except ValueError:
            print(f"Warning: Could not parse coordinates for location: {location}")

    # Create the map
    tracker.create_map(locations)

if __name__ == "__main__":
    main()