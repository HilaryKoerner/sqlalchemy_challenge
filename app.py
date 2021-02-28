#import flask
from flask import Flask, jsonify

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
    return('test precip')


#/api/v1.0/station route
@app.route("/api/v1.0/station")
def station():
    return('test station')

#/api/v1.0/tobs route
@app.route("/api/v1.0/tobs")
def tobs():
    return('test tobs')

#always end with this
if __name__ == "__main__":
    app.run(debug=False)
