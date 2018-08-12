import numpy as np
from datetime import datetime

import pandas as pd
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def routes():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )
@app.route("/api/v1.0/precipitation")
def prcp():
    """Return a list of all dates and temperature observations from the last year"""
    # Query all dates and temps
    prcp_results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= '2016-08-23').all()
    prcp_dict = pd.DataFrame(prcp_results).set_index('date').rename(columns={'prcp': 'Precipitation'}).to_dict()
    
    return jsonify(prcp_dict)  

@app.route("/api/v1.0/stations")
def stations():
    """Return a list of stations from the dataset"""
    # Query all stations
    sta_results = session.query(Station.station, Station.name).filter.all()
    stations_dict = pd.DataFrame(sta_results).set_index('date').rename(columns={'tobs': 'Temperature Observations'}).to_dict()
    
    return jsonify(stations_dict)  

@app.route("/api/v1.0/tobs")
def tobs():
    """Return a list of all dates and temperature observations from the last year"""
    # Query all dates and temps
    tobs_results = session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= '2016-08-23').all()
    tobs_dict = pd.DataFrame(tobs_results).set_index('date').rename(columns={'tobs': 'Temperature Observations'}).to_dict()
    
    return jsonify(tobs_dict)  

@app.route("/api/v1.0/<start>")
def find_tobs_start(start='start_date'):
    start_date = datetime.strptime('2016-08-01', '%Y-%m-%d').date()

    tobs_start_results = session.query(func.max(Measurement.tobs).label("max_tobs"), \
                      func.min(Measurement.tobs).label("min_tobs"),\
                      func.avg(Measurement.tobs).label("avg_tobs")).\
                      filter(Measurement.date >= start_date)   
     
    start_tobs = []
    for tobs in tobs_start_results:
        tobs_dict = {}
        tobs_dict["TAVG"] = float(tobs[2])
        tobs_dict["TMAX"] = float(tobs[0])
        tobs_dict["TMIN"] = float(tobs[1])
        
        start_tobs.append(tobs_dict)

    return jsonify(start_tobs)

@app.route("/api/v1.0/<start>/<end>")
def tobs_start_end(start='start_date', end='end_date'):
    start_date = datetime.strptime('2016-08-01', '%Y-%m-%d').date()
    end_date = datetime.strptime('2016-08-01', '%Y-%m-%d').date()

    start_end_results = session.query(func.max(Measurement.tobs).label("max_tobs"), \
                      func.min(Measurement.tobs).label("min_tobs"),\
                      func.avg(Measurement.tobs).label("avg_tobs")).\
                      filter(Measurement.date.between(start_date, end_date))  

    start_end_tobs = []
    for tobs in start_end_results:
        tobs_dict = {}
        tobs_dict["TAVG"] = float(tobs[2])
        tobs_dict["TMAX"] = float(tobs[0])
        tobs_dict["TMIN"] = float(tobs[1])
        
        start_end_tobs.append(tobs_dict)

    return jsonify(start_end_tobs)

if __name__ == '__main__':
    app.run(debug=True)
