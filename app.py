#import SQL mods
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#import flask
from flask import Flask, jsonify

############
#database setup
#################

# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Stations = Base.classes.station

#create an app and pass __name__
app = Flask(__name__)

#create date and prcp dictionary
nan = 'nan'

prcp_dict = {}

#create an app and pass __name__
app = Flask(__name__)

#index route
@app.route("/")
def home():
    
    print("Server received requst for 'Home' page...")
    return (
        f"Welcome to my SQL Alchemy API<br/>"
        f'Available Routes:<br/>'
        f'/api/v1.0/precipitation<br/>'
        f'/api/v1.0/station<br/>'
        f'/api/v1.0/tobs<br/>'
    )

#/api/v1.0/precipitation route
@app.route("/api/v1.0/precipitation")
def precip():
    #create session route (link from python to DB)
    session = Session(engine)

    prcp_info = session.query(Measurement.date, Measurement.prcp).all()
    #always close the session after the query
    session.close()

    #unpack the tuples
    prcp_list = list(np.ravel(prcp_info))

    return jsonify(prcp_list)


#/api/v1.0/station route
@app.route("/api/v1.0/station")
def station():
    #create session route (link from python to DB)
    session = Session(engine)

    stations = session.query(Stations.station).all()
    #always close the session after the query
    session.close()

    #unpack the tuples
    station_list = list(np.ravel(stations))

    return jsonify(station_list)

#/api/v1.0/tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    #create session route (link from python to DB)
    session = Session(engine)

    station_data = session.query(Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').\
    order_by((Measurement.date).desc()).all()
    #always close the session after the query
    session.close()

    #unpack the tuples
    #station_data_list = list(np.ravel(station_data))
    station_data_list = [result[0] for result in station_data]

    return jsonify(station_data_list)

#merge two tables

#always end with this
if __name__ == "__main__":
    app.run(debug=False)
