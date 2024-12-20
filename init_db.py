import sqlite3
import os
from datetime import datetime, timedelta


def init_database():
    # Remove existing database file if exists
    if os.path.exists('db.sqlite'):
        os.remove('db.sqlite')

    # Create connection
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()

    # Create table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS banknote_history (
            serial_number TEXT,
            location TEXT,
            timestamp TEXT
        )
    """)

    # Sample data
    sample_data = [
        ('CH123001', '46.9481,7.4474, Bern, Switzerland', '2024-06-01 09:30:00')
        ('CH123001', '47.3769,8.5417, Zürich, Switzerland', '2024-06-03 14:15:00')
        ('CH123001', '46.2044,6.1432, Geneva, Switzerland', '2024-06-05 16:45:00')
        ('CH987002', '46.5197,6.6323, Lausanne, Switzerland', '2024-06-02 11:00:00')
        ('CH987002', '47.0502,8.3093, Lucerne, Switzerland', '2024-06-04 13:00:00')
        ('CH456003', '46.0215,7.7479, Zermatt, Switzerland', '2024-06-06 17:30:00')
        ('CH456003', '46.0132,8.9274, Lugano, Switzerland', '2024-06-08 10:15:00')
        ('CH789004', '47.3690,8.5380, Zürich Old Town, Switzerland', '2024-06-09 09:00:00')
        ('CH789004', '47.5596,7.5886, Basel, Switzerland', '2024-06-10 12:45:00')
        ('CH345005', '46.1270,8.6180, Locarno, Switzerland', '2024-06-12 15:15:00')
        ('CH345005', '47.4245,9.3767, St. Gallen, Switzerland', '2024-06-14 18:30:00')
        ('CH678006', '46.2083,6.1460, Geneva Lake, Switzerland', '2024-06-15 11:45:00')
        ('CH678006', '46.9481,7.4474, Bern, Switzerland', '2024-06-17 09:30:00')
        ('CH567007', '46.8800,8.2096, Engelberg, Switzerland', '2024-06-18 13:00:00')
        ('CH567007', '46.8182,8.2275, Andermatt, Switzerland', '2024-06-20 14:30:00')
        ('CH234008', '47.4810,8.2115, Baden, Switzerland', '2024-06-21 16:45:00')
        ('CH234008', '47.0502,8.3093, Lucerne, Switzerland', '2024-06-23 17:30:00')
        ('CH345009', '46.4978,9.8390, St. Moritz, Switzerland', '2024-06-24 09:00:00')
        ('CH345009', '46.0215,7.7479, Zermatt, Switzerland', '2024-06-26 10:30:00')
        ('CH123010', '46.5197,6.6323, Lausanne, Switzerland', '2024-06-27 11:15:00')
        ('CH123010', '47.3769,8.5417, Zürich, Switzerland', '2024-06-29 12:30:00')
        ('CH789011', '46.2044,6.1432, Geneva, Switzerland', '2024-06-30 14:00:00')
        ('CH789011', '47.5596,7.5886, Basel, Switzerland', '2024-07-01 16:45:00')
        ('CH567012', '46.1270,8.6180, Locarno, Switzerland', '2024-07-02 18:00:00')
        ('CH567012', '47.4245,9.3767, St. Gallen, Switzerland', '2024-07-04 20:30:00')
    ]

    # Insert sample data
    cursor.executemany(
        'INSERT INTO banknote_history VALUES (?, ?, ?)', sample_data)

    # Commit and close
    conn.commit()
    conn.close()

    print("Database initialized with sample data!")

    # Test query to verify data
    conn = sqlite3.connect('db.sqlite')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM banknote_history')
    print("\nVerifying data:")
    for row in cursor.fetchall():
        print(f"Serial: {row[0]}, Location: {row[1]}, Time: {row[2]}")
    conn.close()


if __name__ == "__main__":
    init_database()
