import time
import datetime
import requests
import traceback
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, Float, String, DateTime, insert

bike_key = "7479d89868fa2d94fed820aa4ae3379d64bca75f"
contract_name = "Dublin"
bike_URI = "https://api.jcdecaux.com/vls/v1/stations"

weather_key = "836e60d545402f71b66015366f7b8997"
weather_URI = "https://api.openweathermap.org/data/2.5/weather"

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

def get_weather(lon, lat, station_num):
    def get_each_weather(obj, station_num):
        return {"date_created": datetime.datetime.now().replace(microsecond=0),
                "station_number": station_num,
                "pos_lng": obj["coord"]["lon"],
                "pos_lat": obj["coord"]["lat"],
                "weather_id": obj["weather"][0]["id"],
                "main": obj["weather"][0]["main"],
                "description": obj["weather"][0]["description"],
                "icon": obj["weather"][0]["icon"],
                "base": obj["base"],
                "temp": obj["main"]["temp"],
                "feels_like": obj["main"]["feels_like"],
                "temp_min": obj["main"]["temp_min"],
                "temp_max": obj["main"]["temp_max"],
                "pressure": obj["main"]["pressure"],
                "humidity": obj["main"]["humidity"],
                "visibility": obj["visibility"],
                "wind_speed": obj["wind"]["speed"],
                "wind_deg": obj["wind"]["deg"],
                "clouds_all": obj["clouds"]["all"],
                "last_update": datetime.datetime.fromtimestamp(int(obj["dt"] / 1e3)),
                "sys_type": obj["sys"]["type"],
                "sys_id": obj["sys"]["id"],
                "sunrise": datetime.datetime.fromtimestamp(int(obj["sunrise"] / 1e3)),
                "sunset": datetime.datetime.fromtimestamp(int(obj["sunset"] / 1e3)),
                "timezone": obj["timezone"],
                "id": obj["id"],
                "cod": obj["cod"],
                }

    weather_request = requests.get(weather_URI, params={"APPID": weather_key, "lon": lon, "lat": lat})
    weather_data = get_each_weather(weather_request.json(), station_num)
    return weather_data

def write_to_file(obj):
    now = datetime.datetime.now()
    now_format = now.strftime("%Y%m%d_%H%M%S")
    with open("availability_{}".format(now_format), "w") as f:
        f.write(obj)

def scrape_and_store():
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

    weather = Table(
        "weather", meta,
        Column("date_created", DateTime),
        Column("station_number", Integer),
        Column("pos_lng", Float),
        Column("pos_lat", Float),
        Column("weather_id", String(128)),
        Column("main", String(128)),
        Column("description", String(128)),
        Column("icon", String(128)),
        Column("base", String(128)),
        Column("temp", Float),
        Column("feels_like", Float),
        Column("temp_min", Float),
        Column("temp_max", Float),
        Column("pressure", Float),
        Column("humidity", Float),
        Column("visibility", Float),
        Column("wind_speed", Float),
        Column("wind_deg", Float),
        Column("clouds_all", Float),
        Column("last_update", DateTime),
        Column("sys_type", Integer),
        Column("sys_id", Integer),
        Column("sunrise", DateTime),
        Column("sunset", DateTime),
        Column("timezone", Integer),
        Column("name", String(128)),
        Column("id", Integer),
        Column("cod", Integer),
    )

    meta.create_all(engine)
    r = requests.get(bike_URI, params={"apiKey": bike_key, "contract": contract_name})
    station_values = list(map(get_station, r.json()))
    ins_stations = stations.insert().values(station_values)
    engine.execute(ins_stations)
    write_to_file(r.text)
    availability_values = list(map(get_availability, r.json()))
    ins_availability = availability.insert().values(availability_values)
    engine.execute(ins_availability)
    for i in station_values:
        station_num = i["number"]
        longitude = i["pos_lng"]
        latitude = i["pos_lat"]
        weather_values = get_weather(*(str(longitude), str(latitude), station_num))
        ins_weather = weather.insert().values(weather_values)
        engine.execute(ins_weather)

def main():
    while True:
        try:
            scrape_and_store()
            time.sleep(5 * 60)
        except:
            print(traceback.format_exc())

if __name__ == "__main__":
    main()
