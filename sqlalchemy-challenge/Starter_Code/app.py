# Import the dependencies.
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import Column, Integer, String, Float, Boolean

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station
# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
from flask import Flask, jsonify
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route("/")
def homepage():
    return (
    f"Welcome to the Home Page. Here are all the available routes: <br/>
    f"<br/>
    f"Precipitation: /api/v1.0/precipitation
    f"<br/>
    f"Stations: /api/v1.0/stations
    f"<br/>
    f"tobs: /api/v1.0/tobs
    f"<br/>
    f"Temperature data for given start date: /api/v1.0/<start>
    f"<br/>
    f"Temperature data for a given date range: /api/v1.0/<start>/<end>
    )

@app.route("/api/v1.0/precipitation")
def precip():
    session = Session(engine)
    twelve_months = session.query(measurement.date, measurement.prcp).filter(measurement.date >= "2016-08-23").\
order_by(measurement.date.desc())
    session.close()
    
    precip_data = []
    for date, prcp in twelve_months:
        precip_dict = {}
        precip_dict['date'] = date
        precip_dict['precipitation'] = prcp
        precip_data.append(precip_dict)
        
    return(
        jsonify(precip_data)
    )

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    active_stations = session.query(measurement.station, func.count(measurement.station)).group_by(measurement.station).\
order_by(func.count(measurement.station).desc())
    session.close()
    
    station_data = []
    for station, count in active_stations:
        station_dict = {}
        station_dict['station'] = station
        station_dict['measurement_count'] = count
        station_data.append(station_dict)
        
    return(
        jsonify(station_data)
    )

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    
    stats = session.query(measurement.station, func.max(measurement.tobs), func.min(measurement.tobs), func.avg(measurement.tobs)).\
filter(measurement.station == "USC00519281").all()
    
    most_active_twelve_tobs = session.query(measurement.tobs, func.count(measurement.tobs)).filter(measurement.station == "USC00519281").\
filter(measurement.date >= '2016-08-18').group_by(measurement.tobs).order_by(measurement.tobs.asc()).all()
    
    session.close()
    
    tobs_data = []
    for tobs, count in most_active_twelve_tobs:
        tobs_dict = {}
        tobs_dict['Temperature'] = tobs
        tobs_data.append(tobs_dict)
        
    return(
        jsonify(tobs_data)
    )


    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    

        
    