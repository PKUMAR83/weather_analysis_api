from flask import Flask, request, jsonify
from sqlalchemy import create_engine, Column, Integer, String, Date, DECIMAL, ForeignKey, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

app = Flask(__name__)

# Database setup
engine = create_engine('sqlite:///weather_data_api.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class WeatherStation(Base):
    __tablename__ = 'weather_stations'

    station_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)

    records = relationship('WeatherRecord', back_populates='station')


class WeatherRecord(Base):
    __tablename__ = 'weather_records'

    record_id = Column(Integer, primary_key=True,autoincrement=True)
    station_id = Column(Integer, ForeignKey('weather_stations.station_id'))
    date = Column(Date, nullable=False)
    max_temp = Column(DECIMAL(5, 1), nullable=False)
    min_temp = Column(DECIMAL(5, 1), nullable=False)
    precipitation = Column(DECIMAL(5, 1), nullable=False)

    station = relationship('WeatherStation', back_populates='records')


class YearlyWeatherStats(Base):
    __tablename__ = 'yearly_weather_stats'

    id = Column(Integer, primary_key=True, autoincrement=True)
    station_id = Column(Integer, ForeignKey('weather_stations.station_id'))
    year = Column(Integer, nullable=False)
    avg_max_temp = Column(DECIMAL(5, 1))
    avg_min_temp = Column(DECIMAL(5, 1))
    total_precipitation = Column(DECIMAL(5, 1))

    station = relationship('WeatherStation')


Base.metadata.create_all(engine)
