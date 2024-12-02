# Import the dependencies.
import numpy as np
import sqlalchemy
import datetime as dt
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")


# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
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
def welcome():
    return (
        f"Welcome to the Climate API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():

    last_date = session.query(func.max(Measurement.date)).scalar()
    last_year = dt.datetime.strptime(last_date, "%Y-%m-%d") - dt.timedelta(days=365)
    
  
    results = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= last_year).all()


    precip_data = {date: prcp for date, prcp in results}

    return jsonify(precip_data)

@app.route("/api/v1.0/stations")
def stations():

    results = session.query(Station.station).all()

  
    stations_list = [station[0] for station in results]

    return jsonify(stations_list)

@app.route("/api/v1.0/tobs")
def tobs():

    most_active_station = session.query(Measurement.station).\
        group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).first()[0]

   
    last_date = session.query(func.max(Measurement.date)).scalar()
    last_year = dt.datetime.strptime(last_date, "%Y-%m-%d") - dt.timedelta(days=365)

    
    results = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == most_active_station).\
        filter(Measurement.date >= last_year).all()


    tobs_list = [{date: tobs} for date, tobs in results]

    return jsonify(tobs_list)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temp_stats(start, end=None):

    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]

  
    if not end:
        results = session.query(*sel).filter(Measurement.date >= start).all()
    else:
        
        results = session.query(*sel).filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    temps = list(np.ravel(results))

    return jsonify(temps)

if __name__ == "__main__":
    app.run(debug=True)

with open('/mnt/data/app.py', 'w') as app_file:
    app_file.write(app_with_routes)

"app.py has been updated with the required routes." 