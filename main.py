import cv2
import pytesseract
import sqlite3
import folium
import requests
import os
from datetime import datetime

# Function to get user location using IP geolocation
def get_location():
    try:
        response = requests.get("http://ip-api.com/json/")
        data = response.json()
        return data["lat"], data["lon"], f"{data['city']}, {data['country']}"
    except Exception as e:
        print("Error getting location:", e)
        return None, None, "Unknown"

# Function to capture and process the serial number via webcam
def capture_serial_number():
    print("Press 's' to scan serial number or 'q' to quit.")
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Error accessing webcam.")
            break
        cv2.imshow("Capture Serial Number", frame)
        
        # Check for keypress
        key = cv2.waitKey(1)
        if key == ord("s"):  # Scan serial number
            cv2.imwrite("capture.jpg", frame)
            print("Image captured. Performing OCR...")
            serial_number = pytesseract.image_to_string("capture.jpg").strip()
            print("Detected Serial Number:", serial_number)
            return serial_number
        elif key == ord("q"):  # Quit
            break
    cap.release()
    cv2.destroyAllWindows()
    return None

# Function to search for serial number in SQLite DB
def search_serial_number(serial_number, db_path="db.sqlite"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT location, timestamp FROM banknote_history WHERE serial_number = ?", (serial_number,))
    results = cursor.fetchall()
    conn.close()
    return results

# Function to add current location to DB
def add_location_to_db(serial_number, location, db_path="db.sqlite"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO banknote_history VALUES (?, ?, ?)", (serial_number, location, timestamp))
    conn.commit()
    conn.close()

# Function to generate a Folium map
def create_map(locations, output_file="banknote_map.html"):
    if not locations:
        print("No history to display.")
        return
    # Initialize map at first location
    lat, lon = locations[0][0], locations[0][1]
    banknote_map = folium.Map(location=[lat, lon], zoom_start=5)
    
    # Add markers for all locations
    for idx, (lat, lon, description) in enumerate(locations):
        folium.Marker([lat, lon], popup=f"Stop {idx + 1}: {description}").add_to(banknote_map)
    
    # Save map
    banknote_map.save(output_file)
    print(f"Map saved as {output_file}")

# Main script
def main():
    print("Banknote Tracker - Simplified")
    serial_number = input("Enter serial number manually or press Enter to use webcam: ")
    if not serial_number:
        serial_number = capture_serial_number()
    if not serial_number:
        print("No serial number provided.")
        return
    
    print(f"Looking up serial number: {serial_number}")
    history = search_serial_number(serial_number)
    
    # Display history
    print("History of this banknote:")
    for location, timestamp in history:
        print(f"- {location} at {timestamp}")
    
    # Get current location
    lat, lon, description = get_location()
    if not lat or not lon:
        print("Could not retrieve your location.")
        return
    
    # Add to DB
    add_location_to_db(serial_number, description)
    print("Your location has been added to the banknote's history.")
    
    # Generate map
    locations = [(float(lat), float(lon), description)]  # Current location
    for location, _ in history:
        lat, lon = map(float, location.split(","))
        locations.append((lat, lon, location))
    create_map(locations)

if __name__ == "__main__":
    main()
