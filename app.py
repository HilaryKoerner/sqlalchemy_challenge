#import SQL mods
import numpy as np
import datetime as dt

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
        f'/api/v1.0/start_end<br/>'
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
#############################################################################################
####this works
#/api/v1.0/tobs route
# @app.route("/api/v1.0/tobs")
# def tobs():
#     #create session route (link from python to DB)
#     session = Session(engine)

#     station_data = session.query(Measurement.tobs).\
#     filter(Measurement.station == 'USC00519281').\
#     filter(Measurement.station)
#     order_by((Measurement.date).desc()).all()
#     #always close the session after the query
#     session.close()

#     #unpack the tuples
#     #station_data_list = list(np.ravel(station_data))
#     #station_data_list = [result[0] for result in station_data]

#     return jsonify(station_data)
#################################################################################################

@app.route("/api/v1.0/tobs")
def tobs():
    #create session route (link from python to DB)
    session = Session(engine)

    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    station_data = session.query(Measurement.tobs).\
    filter(Measurement.station == 'USC00519281').\
    filter(Measurement.date> prev_year ).\
    order_by((Measurement.date).desc()).all()
    #always close the session after the query
    session.close()

    tobs = []
    for tob in tobs

    #unpack the tuples
    #station_data_list = list(np.ravel(station_data))
    #station_data_list = [result[0] for result in station_data]

    return jsonify(station_data)







@app.route("/api/v1.0/start/<start>")
def start(start):
    #create session route (link from python to DB)
    session = Session(engine)
    
    station_query = [Measurement.station, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
    print(station_query)

    start_date = session.query(*station_query).\
    filter(Measurement.date >= start).\
    group_by(Measurement.station).all()

    session.close()

    start = []
    for station, min_tob, max_tob, avg_tob in start_date:
        start_dict = {}
        start_dict['Station'] = station
        start_dict['Min Temp'] = min_tob
        start_dict['Max Temp'] = max_tob
        start_dict['Avg Temp'] = avg_tob
        start.append(start_dict)

    return jsonify(start)

@app.route("/api/v1.0/start_end/<start>/<end>")
def start_end(start, end):
    #create session route (link from python to DB)
    session = Session(engine)
    
    station_query = [Measurement.station, func.min(Measurement.tobs), func.max(Measurement.tobs), func.avg(Measurement.tobs)]
    print(station_query)

    start_end_date = session.query(*station_query).\
    filter(Measurement.date >= start).\
    filter(Measurement.date < end).\
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

#always end with this
if __name__ == "__main__":
    app.run(debug=True)




##http://127.0.0.1:5000/api/v1.0/start_end/2015-8-24/2017-8-24