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
        f'/api/v1.0/start<br/>'
        f'/api/v1.0//api/v1.0/start_end<br/>'
    )

#/api/v1.0/precipitation route
@app.route("/api/v1.0/precipitation")
def precip():
    #create session route (link from python to DB)
    session = Session(engine)

    prcp_info = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date).all()
    #always close the session after the query
    session.close()

    #create a dictionary
    all_prcp = []
    for date, prcp in prcp_info:
        prcp_dict = {}
        prcp_dict['date'] = date
        prcp_dict['prcp'] = prcp
        all_prcp.append(prcp_dict)
    #unpack the tuples
    #prcp_list = list(np.ravel(prcp_info))

    return jsonify(all_prcp)


#/api/v1.0/station route
@app.route("/api/v1.0/station")
def station():
    #create session route (link from python to DB)
    session = Session(engine)

    stations = session.query(Stations.station).all()
    #always close the session after the query
    session.close()

    all_stations = []
    for station in stations:
        station_dict={}
        station_dict['station name'] = station
        all_stations.append(station_dict)

    #unpack the tuples
    #station_list = list(np.ravel(stations))

    return jsonify(all_stations)

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
    #station_data_list = [result[0] for result in station_data]

    return jsonify(station_data)


# @app.route('/api/v1.0/start')
# def start():
#     # create session route (link from python to DB)
#     session = Session(engine)

#     station_query = [Measurement.station, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]

#     start_date = session.query(*station_query).\
#     filter(Measurement.date >= '2010-01-01').\
#     group_by(Measurement.station).all()
    
#     session.close()

#     return jsonify(start_date)


@app.route("/api/v1.0/start")
def start_data(start):
    """Fetch the date info where start_date matches
       the path variable supplied by the user, or a 404 if not."""

    # canonicalized = start.replace(" ", "").lower()
    # for date in start_data:
    #     search_term = date_input["start"].replace(" ", "").lower()

    #     if search_term == canonicalized:
    #         return jsonify(date_input)

    return jsonify({"error": f"Character with real_name {start} not found."}), 404


@app.route("/api/v1.0/start_end")
def start_end():
    #create session route (link from python to DB)
    session = Session(engine)
    
    station_query = [Measurement.station, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]

    start_end_date = session.query(*station_query).\
    filter(Measurement.date >= '2015-01-01').\
    filter(Measurement.date < '2017-01-01').\
    group_by(Measurement.station).all()

    session.close()

    start_end = []
    for station, min_tob, max_tob, avg_tob in start_end_date:
        start_end_dict = {}
        start_end_dict['Station'] = station
        start_end_dict['Min Temp'] = min_tob
        start_end_dict['Max Temp'] = max_tob
        start_end_dict['Avg Temp'] = avg_tob
        start_end.append(start_end_dict)

    return jsonify(start_end)
#merge two tables

#always end with this
if __name__ == "__main__":
    app.run(debug=False)
