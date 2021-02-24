import pandas as pd
import json
import time
import datetime
import requests
import traceback
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Float, String, DateTime, insert

api_key = "7479d89868fa2d94fed820aa4ae3379d64bca75f"
contract_name = "Dublin"
stations_URI = "https://api.jcdecaux.com/vls/v1/stations"

host = "dbbikes30830.cfv8ckdtpwoq.us-east-1.rds.amazonaws.com"
db = "dbbikes30830"
name = "janeslevin"
password = "js2021dbbikes"

engine = create_engine(f"mysql+mysqlconnector://{name}:{password}@{host}:3306/{db}", echo=True)

def get_station(obj):
    return {"number": obj["number"],
            "name": obj["name"],
            "address": obj["address"],
            "pos_lng": obj["position"]["lng"],
            "pos_lat": obj["position"]["lat"],
            "bike_stands": obj["bike_stands"]
            }

def get_availability(obj):
    return {"date_created": datetime.datetime.now().replace(microsecond=0),
            "number": obj["number"],
            "bike_stands": obj["bike_stands"],
            "available_bike_stands": obj["available_bike_stands"],
            "available_bikes": obj["available_bikes"],
            "last_update": datetime.datetime.fromtimestamp(int(obj["last_update"] / 1e3))
            }

def write_to_file(obj):
    now = datetime.datetime.now()
    now_format = now.strftime("%Y%m%d_%H%M%S")
    with open("availability_{}".format(now_format), "w") as f:
        f.write(obj)

#organise main function
def main():
    meta = MetaData()
    stations = Table(
        "stations", meta,
        Column("number", Integer, primary_key=True),
        Column("name", String(128)),
        Column("address", String(128)),
        Column("pos_lat", Float),
        Column("pos_lng", Float),
        Column("bike_stands", Integer)
    )

    availability = Table(
        "availability", meta,
        Column("date_created", DateTime),
        Column("number", Integer),
        Column("bike_stands", Integer),
        Column("available_bike_stands", Integer),
        Column("available_bikes", Integer),
        Column("last_update", DateTime)
    )

    meta.create_all(engine)
    r = requests.get(stations_URI, params={"apiKey": api_key, "contract": contract_name})
    station_values = list(map(get_station, r.json()))
    ins_stations = stations.insert().values(station_values)
    engine.execute(ins_stations)
    while True:
        try:
            r = requests.get(stations_URI, params={"apiKey": api_key, "contract": contract_name})
            write_to_file(r.text)
            availability_values = list(map(get_availability, r.json()))
            ins_availability = availability.insert().values(availability_values)
            engine.execute(ins_availability)
            time.sleep(5 * 60)
        except:
            print(traceback.format_exc())


if __name__ == "__main__":
    main()
