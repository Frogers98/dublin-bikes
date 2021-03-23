from flask import render_template, url_for, flash, redirect, jsonify
from DB_Flask_App.models import *
from DB_Flask_App import app
import json


@app.route("/")
@app.route("/index")
def station_example():
    """Test to return the stations"""
    
    all_stations=(
                    Station
                        .query
                        .all()
                 )

    filter_station=(
                    Station
                        .query
                        .filter_by(number=10)
                        .first()
                 )

    id_station=(
                    Station
                        .query
                        .get(10)
                 )

    station_avail_data=(
                filter_station
                    .station_availability
                )


    print_statement="<h1>The stations are:</h1><br>"
    print(station_avail_data)
    #for station in all_stations:
        #print_statement+="{}<br>".format(station.name)

    station_dict=Station.to_df()
    print(station_dict)
    print(Station.query.all()[0].to_dict())

    return render_template('index.html',stationname=station_dict.to_json(orient='records'))

