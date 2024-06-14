import os
import sqlite3
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
def ingest_weather_data(directory):
    # Connect to SQLite database
    conn = sqlite3.connect('../db/weather_crop.db')
    start_time = datetime.now()
    records_ingested = 0
    logging.info('Data ingestion started.')
    cursor = conn.cursor()

    # Process each file in the directory
    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            station_name = os.path.splitext(filename)[0]
            station_location = "Unknown Location"  # Placeholder, change as needed

            # Insert weather station if not exists
            cursor.execute('''
                INSERT OR IGNORE INTO weather_station (name, location)
                VALUES (?, ?)
                ''', (station_name, station_location))
            cursor.execute('SELECT id FROM weather_station WHERE name = ?', (station_name,))
            station_id = cursor.fetchone()[0]

            # Read and process weather data file
            filepath = os.path.join(directory, filename)
            with open(filepath, 'r') as file:
                logging.info(f'Processing records from {filename}...')
                for line in file:
                    date_str, max_temp, min_temp, precipitation = line.strip().split('\t')
                    date = datetime.strptime(date_str, '%Y%m%d').date()
                    max_temp = int(max_temp) if max_temp != '-9999' else None
                    min_temp = int(min_temp) if min_temp != '-9999' else None
                    precipitation = int(precipitation) if precipitation != '-9999' else None

                    # Insert weather data with conflict handling
                    cursor.execute('''
                        INSERT OR IGNORE INTO weather_data (station_id, date, max_temp, min_temp, precipitation)
                        VALUES (?, ?, ?, ?, ?)
                        ''', (station_id, date, max_temp, min_temp, precipitation))
                    records_ingested += 1
                logging.info(f'Processing records in {filename} completed.')
    # Commit changes and close connection
    conn.commit()

    #conn.close()
    end_time = datetime.now()
    logging.info(f'Weather Data ingestion completed. {records_ingested} records ingested.')
    logging.info(f'Start time: {start_time}')
    logging.info(f'End time: {end_time}')
    # Calculate and store weather statistics
    calculate_and_store_statistics(conn)

    conn.close()


def calculate_and_store_statistics(conn):
    cursor = conn.cursor()
    start_time = datetime.now()
    records_ingested = 0
    logging.info('Weather statistics ingestion started.')
    # Get unique station_id and year combinations
    cursor.execute('''
    SELECT station_id, strftime('%Y', date) AS year
    FROM weather_data
    GROUP BY station_id, year
    ''')
    station_years = cursor.fetchall()

    for station_id, year in station_years:
        cursor.execute('''
        SELECT 
            AVG(max_temp)/10.0 AS avg_max_temp,
            AVG(min_temp)/10.0 AS avg_min_temp,
            SUM(precipitation)/100.0 AS total_precipitation
        FROM weather_data
        WHERE station_id = ? AND strftime('%Y', date) = ?
        ''', (station_id, year))

        stats = cursor.fetchone()
        avg_max_temp = stats[0]
        avg_min_temp = stats[1]
        total_precipitation = stats[2]

        # Insert statistics into weather_statistics table
        cursor.execute('''
        INSERT OR IGNORE INTO weather_statistics (station_id, year, avg_max_temp, avg_min_temp, total_precipitation)
        VALUES (?, ?, ?, ?, ?)
        ''', (station_id, int(year), avg_max_temp, avg_min_temp, total_precipitation))
        records_ingested += 1
    # Commit changes
    conn.commit()
    end_time = datetime.now()
    logging.info(f'Weather statistics ingestion completed. {records_ingested} records ingested.')
    logging.info(f'Start time: {start_time}')
    logging.info(f'End time: {end_time}')

# Ingest data from the specified directory
ingest_weather_data('../wx_data')
