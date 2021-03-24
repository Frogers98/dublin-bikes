from flask import Flask, request, render_template, url_for
from sqlalchemy import create_engine
import pandas as pd
import json
import pprint
app = Flask(__name__)

def get_stations_json():
    """Returns the stations table as a json string
    The other functions can just call this instead of re-using the code in each function"""
    URI = "dublin-bikes.ciu0f2oznjig.us-east-1.rds.amazonaws.com"
    PORT = "3306"
    DB = "dublin_bikes"
    USER = "admin"
    PASSWORD = "DublinBikesProject2201"
    engine = create_engine('mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(USER, PASSWORD, URI, PORT, DB, echo=True))
    print("in get_stations_json()")
    df = pd.read_sql_table("01_station", engine)
    station_json = df.to_json(orient="records")
    print("station data type:", type(station_json))
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(station_json)
    print()
    return station_json

@app.route("/")
def hello():
    # Get the stations object as a json string
    stations = get_stations_json()
    # Convert the json string to a dictionary so python can iterate through it
    stations = json.loads(stations)
    print(stations)
    return render_template("index.html", station_data = stations)

@app.route("/stations")
def stations_request():
    print("in /stations")
    stations = get_stations_json()
    return stations

@app.route("/availability")
def availability_request():
    print("IN AVAILABILITY FUNCTION")
    URI = "dublin-bikes.ciu0f2oznjig.us-east-1.rds.amazonaws.com"
    PORT = "3306"
    DB = "dublin_bikes"
    USER = "admin"
    PASSWORD = "DublinBikesProject2201"
    engine = create_engine('mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(USER, PASSWORD, URI, PORT, DB, echo=True))

    sql = """SELECT * FROM dublin_bikes.01_availability
    ORDER BY created_date DESC
    LIMIT 109; """
    result = engine.execute(sql)
    print("type of sql request is", type(result))
    for number, available_bikes, available_bike_stands, last_update, created_date in result:
        print("number is:", number, "available bikes is:", available_bikes, "available_bike_stands is:", available_bike_stands, "last update is:", last_update, "created date is:", created_date)
    return json.dumps(result)

if __name__ == '__main__':
    app.run(debug=True)