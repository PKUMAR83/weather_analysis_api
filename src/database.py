import sqlite3

def create_database():
    # Connect to SQLite database
    conn = sqlite3.connect('../db/weather_crop.db')
    cursor = conn.cursor()

    # Create weather_station table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS weather_station (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        location TEXT NOT NULL
    )
    ''')

    # Create weather_data table with unique constraint
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS weather_data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        station_id INTEGER,
        date DATE,
        max_temp INTEGER,
        min_temp INTEGER,
        precipitation INTEGER,
        UNIQUE(station_id, date),
        FOREIGN KEY (station_id) REFERENCES weather_station(id)
    )
    ''')

    # Create weather_statistics table with unique constraint
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS weather_statistics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        station_id INTEGER,
        year INTEGER,
        avg_max_temp REAL,
        avg_min_temp REAL,
        total_precipitation REAL,
        UNIQUE(station_id, year),
        FOREIGN KEY (station_id) REFERENCES weather_station(id)
    )
    ''')

    # Create crop_field table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS crop_field (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        location TEXT NOT NULL
    )
    ''')

    # Create crop_yield table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS crop_yield (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        field_id INTEGER,
        year INTEGER,
        yield REAL,
        FOREIGN KEY (field_id) REFERENCES crop_field(id)
    )
    ''')

    # Commit changes and close connection
    conn.commit()
    conn.close()

