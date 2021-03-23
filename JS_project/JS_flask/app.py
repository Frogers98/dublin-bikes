from flask import Flask, render_template
import sqlalchemy as sqla
import json
import pandas as pd

app = Flask(__name__)

def createEngine():
    host = "dbbikes30830.cfv8ckdtpwoq.us-east-1.rds.amazonaws.com"
    db = "dbbikes30830"
    name = "janeslevin"
    password = "js2021dbbikes"

    engine = sqla.create_engine(f"mysql+mysqlconnector://{name}:{password}@{host}:3306/{db}", echo=True)
    return engine

def requestStationData():
    engine = createEngine()
    # Read sql database table into a dataframe
    df = pd.read_sql_table("01_station", engine)
    print(df.iloc[1])
    # Convert to JSON string
    stationJSON = df.to_json(orient="records")

    return stationJSON

def requestAvailabilityData():
    engine = createEngine()
    metadata = sqla.MetaData()
    station_data = sqla.Table('01_station', metadata, autoload=True, autoload_with=engine)
    print(station_data.columns.keys())

@app.route("/")
def index():
    # Convert JSON string to python dictionary
    stationDict = json.loads(requestStationData())
    return render_template("index.html", stationDict = stationDict)

@app.route("/stations")
def stations():
    stationData = requestStationData()
    return stationData

@app.route("/availability")
def recentUpdate():
    engine = createEngine()
    engine.connect()

    metadata = sqla.MetaData()
    availability_data = sqla.Table('01_availability', metadata, autoload=True, autoload_with=engine)
    query = sqla.select([availability_data]).order_by(sqla.desc(availability_data.columns.created_date)).limit(109)
    df = pd.read_sql_query(query, engine)
    print(df.iloc[:10])

    return ""

if __name__ == "__main__":
    app.run(debug=True)
