import numpy as np
from datetime import datetime
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
session = Session(engine)

#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Welcome to the Hawaii Climate Analysis API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp/start/end<br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():

    # Query all prcp values
    last_12m = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= last_12m).all()

    session.close()

    # Convert list of tuples into normal list
    #past_12m_prcp = list(np.ravel(results))
    past_12m_prcp = {date: prcp for date, prcp in results}

    return jsonify(past_12m_prcp)


@app.route("/api/v1.0/station")
def station():
    results = session.query(Station).all()
    session.close()

    # Create a dictionary from the row data and append to a list of stations
    stations = []
    for stationvar in results:
        station_dict = {}
        station_dict["station"] = stationvar.station
        stations.append(station_dict)

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    results = session.query(Measurement.tobs).filter(Measurement.date >= last_12m).all()
    session.close()

    # Create a dictionary from the row data and append to a list of tobs
    temp_list = []
    for temp in results:
        temp_dict = {}
        temp_dict["Temperatures"] = float(temp)
        temp_list.append(temp_dict)

    return jsonify(temp_list)

@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
def stats(start=None, end=None):
    session = Session(engine)
    
    if not end:
        results = session.query(*[[func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]]).filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps)

    results = session.query(*[[func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]]).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    temps = list(np.ravel(results))
    return jsonify(temps)
    return jsonify(trip_temps)

if __name__ == '__main__':
    app.run(debug=True)
