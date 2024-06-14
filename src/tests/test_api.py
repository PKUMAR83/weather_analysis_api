import unittest
import sqlite3
from flask import Flask
from flask_testing import TestCase
import os

class TestWeatherCropAPI(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.config['TESTING'] = True
        app.config['DATABASE'] = 'test_weather_crop.db'
        return app

    def setUp(self):
        # Set up a temporary database for testing
        conn = sqlite3.connect('test_weather_crop.db')
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather_station (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT NOT NULL
        )
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS weather_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            station_id INTEGER,
            date DATE,
            max_temp INTEGER,
            min_temp INTEGER,
            precipitation INTEGER,
            FOREIGN KEY (station_id) REFERENCES weather_station(id)
        )
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS crop_field (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            location TEXT NOT NULL
        )
        ''')
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS crop_yield (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            field_id INTEGER,
            year INTEGER,
            yield REAL,
            FOREIGN KEY (field_id) REFERENCES crop_field(id)
        )
        ''')
        conn.commit()
        conn.close()

    def tearDown(self):
        # Remove the temporary database
        os.remove('test_weather_crop.db')

    def test_weather_summary(self):
        # Example test for weather summary endpoint
        conn = sqlite3.connect('test_weather_crop.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO weather_station (name, location) VALUES (?, ?)', ('Station1', 'Location1'))
        cursor.execute('SELECT id FROM weather_station WHERE name = ?', ('Station1',))
        station_id = cursor.fetchone()[0]
        cursor.execute('''
        INSERT INTO weather_data (station_id, date, max_temp, min_temp, precipitation)
        VALUES (?, ?, ?, ?, ?)
        ''', (station_id, '2020-01-01', 100, 50, 10))
        conn.commit()
        conn.close()

        response = self.client.get(f'/weather/{station_id}/2020')
        self.assertEqual(response.status_code, 200)
        self.assertIn('avg_max_temp', response.json)
        self.assertIn('avg_min_temp', response.json)
        self.assertIn('total_precipitation', response.json)

    def test_crop_yield(self):
        # Example test for crop yield endpoint
        conn = sqlite3.connect('test_weather_crop.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO crop_field (name, location) VALUES (?, ?)', ('Field1', 'Location1'))
        cursor.execute('SELECT id FROM crop_field WHERE name = ?', ('Field1',))
        field_id = cursor.fetchone()[0]
        cursor.execute('''
        INSERT INTO crop_yield (field_id, year, yield)
        VALUES (?, ?, ?)
        ''', (field_id, 2020, 100.0))
        conn.commit()
        conn.close()

        response = self.client.get(f'/crop_yield/{field_id}/2020')
        self.assertEqual(response.status_code, 200)
        self.assertIn('field_id', response.json)
        self.assertIn('year', response.json)
        self.assertIn('yield', response.json)

if __name__ == '__main__':
    unittest.main()
