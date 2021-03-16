from flask import Flask, request, render_template, url_for
from sqlalchemy import create_engine
import pandas as pd
import json
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
    return station_json

@app.route("/")
def hello():
    # Get the stations object as a json string
    stations = get_stations_json()
    # Convert the json string to a dictionary so python can iterate through it
    stations = json.loads(stations)
    print(stations)
    return render_template("index.html", station_data = stations)

@app.route("/tables")
def get_tables():
    """Function to just display the first five rows of each database table as a table on the webpage"""
    URI = "dublin-bikes.ciu0f2oznjig.us-east-1.rds.amazonaws.com"
    PORT = "3306"
    DB = "dublin_bikes"
    USER = "admin"
    PASSWORD = "DublinBikesProject2201"
    engine = create_engine('mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(USER, PASSWORD, URI, PORT, DB, echo=True))

    station_df = pd.read_sql_table("01_station", engine, chunksize = 50)
    station_df_html = station_df.head(5).to_html()

    weather_df = pd.read_sql_table("01_weather", engine, chunksize = 50)
    weather_df_html = weather_df.head(5).to_html()

    availability_df = pd.read_sql_table("01_availability", engine, chunksize = 50)
    availability_df_html = availability_df.head(5).to_html()

    #station_json = df.to_json(orient="records")
    return render_template("table.html", tables=[station_df_html, weather_df_html, availability_df_html])

@app.route("/stations")
def stations_request():
    print("in /stations")
    stations = get_stations_json()
    return stations
if __name__ == '__main__':
    app.run(debug=True)