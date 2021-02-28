#import flask
from flask import flask

#create an app and pass __name__
app = Flask(__name__)

#index route
@app.route("/")
def home():
    







#always end with this
if __name__ == "__main__":
    app.run(debug=True)
