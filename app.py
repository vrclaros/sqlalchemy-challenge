import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# if you wish to isolate the connection
# engine.execute("select * from table")

# connection=engine.connect()

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
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temperature/<start><br/>"
        f"/api/v1.0/temperature/<start>/<end><br/>"

    )


@app.route("/api/v1.0/precipitation")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a date and prcp"""
    # Query all 
    results = session.query(Measurement.date,Measurement.prcp).all()

    session.close()

    # Convert list of tuples into normal list
    all_prcp = {date: prcp for date,prcp in results}

    return jsonify(all_prcp)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations"""
    # Query all stations
    results = session.query(Station.station).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_stations
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return tobs for most active station for one year"""
    # Query all
    results = session.query(Measurement.tobs).filter(Measurement.station == 'USC00519281').filter(Measurement.date >= '2016-08-23').all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_tobs
    all_tobs = list(np.ravel(results))

    return jsonify(all_tobs)

@app.route("/api/v1.0/temperature/<start>")
def temperature(start = None):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return temp with a start date"""
    # Query all 
    results = session.query(func.max(Measurement.tobs),func.min(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date > start).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_temperature
    all_temperature = list(np.ravel(results))

    return jsonify(all_temperature)

@app.route("/api/v1.0/temp/<start>/<end>")
def temp(start = None, end = None):
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return temp with a start date and end date"""
    # Query all 
    results = session.query(func.max(Measurement.tobs),func.min(Measurement.tobs),func.avg(Measurement.tobs)).filter(Measurement.date > start).filter(Measurement.date < end).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_temperature
    all_temperature = list(np.ravel(results))

    return jsonify(all_temperature)

if __name__ == '__main__':
    app.run(debug=True)
