import numpy as np

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
        f"/api/v1.0/temp/start/end"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all passenger names"""
    # Query all passengers
    last_12m = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= last_12m).all()

    session.close()

    # Convert list of tuples into normal list
    #past_12m_prcp = list(np.ravel(results))
    past_12m_prcp = {date: prcp for date, prcp in results}

    return jsonify(past_12m_prcp)


@app.route("/api/v1.0/station")
def station():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    

    results = session.query(Station).all()
    session.close()

    # Create a dictionary from the row data and append to a list of all_stations
    all_stations = []
    for stationvar in results:
        station_dict = {}
        station_dict["station"] = stationvar.station
        all_stations.append(station_dict)

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of passenger data including the name, age, and sex of each passenger"""
    # Query all passengers
    

    results = session.query(Measurement.tobs).all()
    session.close()

    # Create a dictionary from the row data and append to a list of all_stations
    all_stations = []
    for stationvar in results:
        station_dict = {}
        station_dict["station"] = stationvar.station
        all_stations.append(station_dict)

    return jsonify(all_stations)


if __name__ == '__main__':
    app.run(debug=True)
