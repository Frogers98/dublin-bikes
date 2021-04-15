##------------------Extractor---------------##
## 
##User:     Aryan
##DC:       2021-02-15
##DLM:      2021-02-15
##MC:       COMP30830
##SD:       Save Dublin Bike Info
##
##------------------Extractor---------------##



####--------------------------------------
#00.Import Modules
####--------------------------------------

######---------BEGIN
#      ML
######--------END

#import nltk as nl
#import sklearn as sk
#import matplotlib as mp
#import xgboost as xg
#import pymc3 as pymc
#import sympy as sym



######---------BEGIN
#      SQL
######--------END


import requests as rq
import sqlalchemy as sqla
#import pyodbc
#import cx_oracle as cx


######---------BEGIN
#     GENERAL
######--------END

import pandas as pd
import datetime as dt
import numpy as np
#import pyodbc
import sys
import os
import json
import time
import socket
import traceback as tb
import platform
from psutil import virtual_memory

#BeExplicit <- Works for Me Locally but needs to have installed module. Replacing with explicit
#from station_info.data_dictionary import services_dictionary
#from station_info.data_dictionary import database_dictionary
#from station_info.data_dictionary import database_schema


database_dictionary={
                        'username':'adamryan'
                        ,'password':'adam.ryan1'
                        ,'database':'dbbikes'
                        ,'endpoint':'dbbikes.cmbuuvrlonfv.us-east-1.rds.amazonaws.com'
                        ,'port':'3306'    
                    }

database_schema={
                    '01_station':{
                              'address':'VARCHAR(256)'
                              ,'banking':'INTEGER'
                              ,'bike_stands':'INTEGER'
                              ,'bonus':'INTEGER'
                              ,'contract_name':'VARCHAR(256)'
                              ,'name':'VARCHAR(256)'
                              ,'number':'INTEGER'
                              ,'position_lat':'REAL'
                              ,'position_long':'REAL'
                              ,'created_date': 'BIGINT'
                                }
                    ,'01_availability':{
                                'number':'INTEGER'
                                ,'available_bikes':'INTEGER'
                                ,'available_bike_stands':'INTEGER'
                                ,'last_update':'BIGINT'
                                ,'created_date':'BIGINT'
                                }
    
                    ,'01_weather':{
                                'number': 'INT'
                                ,'position_long':'REAL'
                                ,'position_lat':'REAL'
                                ,'weather_id':'INTEGER'
                                ,'main':'VARCHAR(256)'
                                ,'description':'VARCHAR(500)'
                                ,'icon':'VARCHAR(20)'
                                ,'icon_url':'VARCHAR(500)'
                                ,'base':'varchar(256)'
                                ,'temp':'REAL'
                                ,'feels_like':'REAL'
                                ,'temp_min':'REAL'
                                ,'temp_max':'REAL'
                                ,'pressure':'INT'
                                ,'humidity':'INT'
                                ,'visibility':'INT'
                                ,'wind_speed':'REAL'
                                ,'wind_degree':'INT'
                                ,'clouds_all':'INT'
                                ,'datetime':'BIGINT'
                                ,'sys_id':'INT'
                                ,'sys_country':'VARCHAR(10)'
                                ,'sys_sunrise':'BIGINT'
                                ,'sys_sunset':'BIGINT'
                                ,'sys_type':'INT'
                                ,'timezone':'INT'
                                ,'id':'BIGINT'
                                ,'name':'VARCHAR(256)'
                                ,'cod':'INT'
                                ,'created_date':'BIGINT'
                                }

                    ,'01_forecast':{
        # Removed base, timezone, avail_update_dt, datetime, id_var, name, cod and all 'sys' entries when compared to original scraper
        # Added forecast_time_dt and forecast_time_txt to show the forecast times in readable format
                                'number': 'INT'
                                ,'position_long':'REAL'
                                ,'position_lat':'REAL'
                                ,'weather_id':'INTEGER'
                                ,'main':'VARCHAR(256)'
                                ,'description':'VARCHAR(500)'
                                ,'icon':'VARCHAR(20)'
                                ,'icon_url':'VARCHAR(500)'
                                ,'temp':'REAL'
                                ,'feels_like':'REAL'
                                ,'temp_min':'REAL'
                                ,'temp_max':'REAL'
                                ,'pressure':'INT'
                                ,'humidity':'INT'
                                ,'visibility':'INT'
                                ,'wind_speed':'REAL'
                                ,'wind_degree':'INT'
                                ,'clouds_all':'INT'
                                ,'forecast_time_dt':'BIGINT'
                                ,'forecast_time_txt':'VARCHAR(200)'
                                ,'created_date':'BIGINT'
                                }
    
                    ,'02_station_avail_weather_train':{
                                'number':'INTEGER'
                                , 'weather_type_id':'INTEGER'
                                , 'hour':'INTEGER'
                                , 'dayofweek':'INTEGER'
                                , 'dayofmonth':'INTEGER'
                                , 'bool_weekend':'BOOLEAN'
                                , 'bool_dayoff':'BOOLEAN'
                                , 'bool_workhour':'BOOLEAN'
                                , 'bool_commutehour':'BOOLEAN'
                                , 'bool_night':'BOOLEAN'
                                , 'available_bikes':'REAL' #average over everything
                                , 'weather_temp_feels_like':'REAL' #average over everything
                                , 'weather_temp':'REAL' #average over everything
                               ,  'weather_humidity':'REAL' #average over everything
                                , 'weather_air_pressure':'REAL' #average over everything
                                , 'created_date':'BIGINT'
                                }
    
,                   '02_station_avail_weather_test':{
                                'number':'INTEGER'
                                , 'weather_type_id':'INTEGER'
                                , 'hour':'INTEGER'
                                , 'dayofweek':'INTEGER'
                                , 'dayofmonth':'INTEGER'
                                , 'bool_weekend':'BOOLEAN'
                                , 'bool_dayoff':'BOOLEAN'
                                , 'bool_workhour':'BOOLEAN'
                                , 'bool_commutehour':'BOOLEAN'
                                , 'bool_night':'BOOLEAN'
                                , 'available_bikes':'REAL' #average over everything
                                , 'weather_temp_feels_like':'REAL' #average over everything
                                , 'weather_temp':'REAL' #average over everything
                                , 'weather_humidity':'REAL' #average over everything
                                , 'weather_air_pressure':'REAL' #average over everything
                                , 'created_date':'BIGINT'
                                }
    
    ,                   '03_user_model_entry':{
                                'prediction_id':'INTEGER'
                                ,'number':'INTEGER'
                                , 'weather_type_id':'INTEGER'
                                , 'hour':'INTEGER'
                                , 'dayofweek':'INTEGER'
                                , 'dayofmonth':'INTEGER'
                                , 'bool_weekend':'BOOLEAN'
                                , 'bool_dayoff':'BOOLEAN'
                                , 'bool_workhour':'BOOLEAN'
                                , 'bool_commutehour':'BOOLEAN'
                                , 'bool_night':'BOOLEAN'
                                , 'available_bikes':'REAL' #average over everything
                                , 'weather_temp_feels_like':'REAL' #average over everything
                                , 'weather_temp':'REAL' #average over everything
                                , 'weather_humidity':'REAL' #average over everything
                                , 'weather_air_pressure':'REAL' #average over everything
                                , 'user_date':'BIGINT'        
                                , 'created_date':'BIGINT'
                                , 'predicted_date':'BIGINT'
                                , 'model_type':'VARCHAR(100)'
                                , 'bool_correct_prediction':'BOOLEAN'
                                }
                }


services_dictionary={
                'Dublin Bikes':
                    {
                       'Service Provider':'JCDecaux'
                       ,'API Reason':'Dublin Bikes'
                       ,'Security':'secret'
                        
                       ,'Endpoint':{
                           'Station':'https://api.jcdecaux.com/vls/v1/stations'
                           ,'Contract':'https://api.jcdecaux.com/vls/v1/contracts'
                           ,'Park of Contract':'https://api.jcdecaux.com/parking/v1/contracts/{}/parks'
                           ,'Park Info':'https://api.jcdecaux.com/parking/v1/contracts/{}/parks/{}'

                                       }
                        ,'API Key':'fce18e526613c8451be601a23ce591ed36b2b209'
                    },
                'OpenWeatherAPI':
                    {
                        'Service Provider':'OpenWeatherMap'
                        ,'API Reason':'Weather Data'
                        ,'Security':'secret'

                        ,'Endpoint':{
                                'weather_at_coord':'http://api.openweathermap.org/data/2.5/weather' #?lat={}&lon={}&appid={}
                                    }
                        ,'API Key':'fa4a1ef5fe110a5b66dbe8f58890b6f1'
                    },

                'OpenWeatherMapForecast':
                    {
                        'Service Provider':'OpenWeatherMap'
                        ,'API Reason':'Weather Data'
                        ,'Security':'secret'

                        ,'Endpoint':{
                                'weather_at_coord':'http://api.openweathermap.org/data/2.5/forecast' #?lat={}&lon={}&appid={}
                                    }
                        ,'API Key':'fa4a1ef5fe110a5b66dbe8f58890b6f1'
                    },
               }

######---------BEGIN
#     DATA VIS
######--------END

#import seaborn as sb
#import matplotlib as mp
#from bokeh import *
#from dash import *


####--------------------------------------
#01. Conncct to db
####--------------------------------------


def connect_db_engine(host,user,password,port,db):
    """Connect to the db engine
    
    host: host
    user: user
    password: pw
    port: port
    db: Name of DB
    
    
    """
    
    print("Inside connect_db_engine()\n\n")
    
    error_code=0
    engine=''
    
    error_dictionary={0:'No Error'
                     ,1:'One of the parameters is wrong'
                      ,999: 'Uncaught exception'
                     }
    
    try:
        connect_statement='mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(user,password,host,port,db)
        print(connect_statement)
        engine=sqla.create_engine(connect_statement,echo=True)
        
    except Exception as e:
        error_code=999
        print(e)
    
    return [error_code,engine]




####--------------------------------------
#02. Setup DB
####--------------------------------------



def setup_database(host,user,password,port,db):
    """Set up the database if it does not already exist.
    
    Input is the database parameters and database_dictionary
    """
    
    print("Inside setup_database()\n\n")
    
    engine_l=connect_db_engine(host,user,password,port,db)
    engine=engine_l[1]
    
    create_sql="""
                CREATE DATABASE IF NOT EXISTS 
                                            {};
                """.format(db)
    
    engine.execute(create_sql)
    
   
    
    #Loop through every table
    for table, columns in database_schema.items():
        column_count=0
        column_number=len(columns)
        insert_sql=''
        insert_sql="""CREATE TABLE IF NOT EXISTS {} (\n""".format(table)
        insert_row=''
        
        #for every column and type add on a statement
        for column_name, column_type in columns.items():
            
            #Add the statement with , in front
            if column_count>0:
                insert_row+=",{}     {}".format(column_name,column_type)
                
            #First column
            else:
                insert_row+="{}     {}".format(column_name,column_type)
                column_count+=1
                
                
        insert_sql+='{})'.format(insert_row)
        
        #Start this madness re: creating and inserting the schema
        try:
            engine.execute(insert_sql)
            
        #Except for something; probably the schema
        except Exception as exc:
            print(exc)
            
    print('Database Schema Created, have fun!')
    engine.dispose()
    
    return




####--------------------------------------
#03. Retrieve Station Info
####--------------------------------------


####All Stations
SQL_select_station="""
    SELECT
         stat.{}                              AS                      number
        ,stat.{}                              AS                      address
        ,stat.{}                              AS                      banking
        ,stat.{}                              AS                      bike_status
        ,stat.{}                              AS                      bike_stands
        ,stat.{}                              AS                      contract_name
        ,stat.{}                              AS                      name
        ,stat.{}                              AS                      position_lat
        ,stat.{}                              AS                      position_long
        ,FROM_UNIXTIME(stat.{})               AS                      created_date
    FROM
        {} stat
    """.format('number'
            ,'address'
            ,'banking'
            ,'bike_stands'
            ,'bonus'
            ,'contract_name'
            ,'name'
            ,'position_lat'
            ,'position_long'
            ,'created_date'
            ,'01_station')

def station_table_df(host,user,password,port,db):
    """Retrieve the station table.
    
    Return table as dataframe
    """
    
    print("Inside setup_database()\n\n")
    
    engine_l=connect_db_engine(host,user,password,port,db)
    engine=engine_l[1]
    df=pd.DataFrame()

    #no error
    try:
        df=pd.read_sql(SQL_select_station,engine)
    
    except Exception as e:
        print(e)

    engine.dispose()

    return df




####--------------------------------------
#04. Get the weather forecast
####--------------------------------------

def getWeatherForecast(latitude, longitude):
    """Function to return the weather forecast for certain co-ordinates"""
    weather_key = services_dictionary['OpenWeatherMapForecast']['API Key']
    endpoint=services_dictionary['OpenWeatherMapForecast']['Endpoint']['weather_at_coord']
    r = requests.get(endpoint, params={"APPID": weather_key, "lat": latitude, "lon": longitude})
    return r.json()

####--------------------------------------
#05. Store the forecast Info
####--------------------------------------


def store_weather_forecast(weather_json,number,time_added,host,user,password,port,db):
    """
    Store the Weather Data into the database
    Removed base, timezone, avail_update_dt, datetime, id_var, name, cod and all 'sys' entries when compared to scraper for current weather
    Added forecast_time_dt and forecast_time_txt
    """
    
    engine_l=connect_db_engine(host,user,password,port,db)
    engine=engine_l[1]
    
    print('Inside store_weather_forecast')
    station_number=number
    
    print(weather_json)
    
    position_long=weather_json['city']['coord']['lon']
    position_lat=weather_json['city']['coord']['lat']

    for forecast_time in weather_json['list']:
        # Loops through every forecast time at three hour intervals for the next 5 days for the current coordinates and saves it in the database
        forecast_time_dt = forecast_time['dt']
        forecast_time_txt = forecast_time['dt_txt']
        weather_id=forecast_time['weather'][0]['id']
        main=forecast_time['weather'][0]['main']
        description=forecast_time['weather'][0]['description']
        icon=forecast_time['weather'][0]['icon']
        icon_url='http://openweathermap.org/img/wn/{}@2x.png'.format(icon)

        temp=forecast_time['main']['temp']
        feels_like=forecast_time['main']['feels_like']
        temp_min=forecast_time['main']['temp_min']
        temp_max=forecast_time['main']['temp_max']
        pressure=forecast_time['main']['pressure']
        humidity=forecast_time['main']['humidity']
        visibility=forecast_time['visibility']

        wind_speed=forecast_time['wind']['speed']
        wind_degree=forecast_time['wind']['deg']

        clouds_all=forecast_time['clouds']['all']

        created_date=time_added

        weather_insert='''INSERT INTO 01_forecast
    
                                    (    number
                                        ,position_long
                                        ,position_lat
    
                                        ,weather_id
                                        ,main
                                        ,description
                                        ,icon
                                        ,icon_url
    
                                        ,temp
                                        ,feels_like
                                        ,temp_min
                                        ,temp_max
                                        ,pressure
                                        ,humidity
                                        ,visibility
    
                                        ,wind_speed
                                        ,wind_degree
    
                                        ,clouds_all
    
                                        ,forecast_time_dt
                                        ,forecast_time_txt
    
                                        ,created_date)
    
                                VALUES
                                    (%s
                                      ,%s
                                      ,%s
    
                                      ,%s
                                      ,%s
                                      ,%s
                                      ,%s
                                      ,%s
    
                                      ,%s
                                      ,%s
                                      ,%s
                                      ,%s
                                      ,%s
                                      ,%s

    
                                      ,%s
                                      ,%s
    
                                      ,%s
    
                                      ,%s
                                      ,%s
    
                                      ,%s
                                      ,%s)
                                        '''

        weather_values=(station_number
                        ,position_long
                        ,position_lat
                        ,weather_id
                        ,main
                        ,description
                        ,icon
                        ,icon_url
                        ,temp
                        ,feels_like
                        ,temp_min
                        ,temp_max
                        ,pressure
                        ,humidity
                        ,visibility
                        ,wind_speed
                        ,wind_degree
                        ,clouds_all
                        ,forecast_time_dt
                        ,forecast_time_txt
                        ,created_date)

        engine.execute(weather_insert,weather_values)
        
    engine.dispose()

    return



####--------------------------------------
#06. Get the forecast info per station
####--------------------------------------

def forecast_per_station(host,user,password,port,db):
    """Getting the forecast data for each station, leve"""

    setup_database(host,user,password,port,db)
    station_data = station_table_df(host,user,password,port,db)
    
    station_data=json.loads(station_data.to_json(orient='records'))
    print(station_data)
    
    # Set up the forecast table if it hasn't been done already
    #Get the current date for when this function is called to be able to group all entries together
    datetime_now = dt.datetime.now()
    created_date = dt.datetime.timestamp(datetime_now)

    # Loop through each bike station to get their coordinates and make a forecast call on those coordinates
    for station in station_data:
        position_lat = station['position_lat']
        position_lng = station['position_long']
        number = station['number']
        print("**************")
        print(f"Current station is station number {number} ")
        print("**************")
        # Get the forecast for the co-ordinates of the current station in the loop
        weather_json = getWeatherForecast(latitude=position_lat, longitude=position_lng)
        # Store the forecast for this station in the database
        store_weather_forecast(weather_json, number, created_date,host,user,password,port,db)
    print("**************")
    print("Forecasts inserted for all stations!")
    print("**************")
    return
    


def clear_forecast_table(host,user,password,port,db):
    """A function to empty the forecast table"""

    try:
        #Engine
        engine_l=connect_db_engine(host,user,password,port,db)
        engine=engine_l[1]

        #
        enable_delete_SQL="""SET SQL_SAFE_UPDATES = 0"""
        delete_forecast_SQL="""Delete from 01_forecast"""
        disable_delete_SQL="""SET SQL_SAFE_UPDATES = 1"""

        engine.execute(enable_delete_SQL)
        engine.execute(delete_forecast_SQL)
        engine.execute(disable_delete_SQL)

        engine.dispose()
    except Exception as e:
        print("Failed to delete: {}".format(e))

####--------------------------------------
#11. get machine info
####--------------------------------------

def machine_info():
    """Gets some info on your machine"""

    machine_name=platform.machine
    os_name=platform.os
    os_version=platform.version
    host_name=socket.gethostname()
    ip_address=socket.gethostbyname(host_name)
    #total_memory=virtual_memory.total()

    print_statement="""
        Your benchmarketing stats are as follows:\n\n
        machine_name = {}
        os_name= {}
        os_version= {}
        host_name= {}
        ip_address= {}
        total_memory= {}\n\n"""

    print(print_statement.format(machine_name
                            ,os_name
                            ,os_version
                            ,host_name
                            ,ip_address
                            ,'TBD'))

    return

####--------------------------------------
#12. Run Main
####--------------------------------------


def main():
    """Main Function"""
    
    print("Inside Main\n\n")

    machine_info()

    myhost=database_dictionary['endpoint']
    myuser=database_dictionary['username']
    mypassword=database_dictionary['password']
    myport=database_dictionary['port']
    mydb=database_dictionary['database']

    while True:
        
        #Pull it every five miutes
        try:
            print("-------------------------------\n\n\n")
            print("-------------------------------\n\n\n")
            print("-------------------------------\n\n\n")
            print('''Starting: The time now is: {}'''.format(dt.datetime.now()))
            
            #Delay it until 12am to avoid app functionality issue
            t1 = time.time()
            seconds_in_hour=60*60
            seconds_in_day=seconds_in_hour**24

            #Allow operation between 11pm and 1am when time in app is likely low.
            if dt.datetime.now().hour==0 or dt.datetime.now().hour==23 or dt.datetime.now().hour==1:
                clear_forecast_table(host=myhost,user=myuser,password=mypassword,port=myport,db=mydb)
                forecast_per_station(host=myhost,user=myuser,password=mypassword,port=myport,db=mydb) 

            else:
                print("Outside of operation time")


            runtime=time.time()-t1
            time.sleep(seconds_in_day - runtime)
            print('\n\n\n------------------------------')
            print('\n\n\n------------------------------')
            print('\n\n\n------------------------------')
            print('\n\n\n------------------------------')
            
        #Error so figure out what it is.
        except Exception as e:
            print(e)
            
    return


###RUN MAIN!!!

if __name__ == '__main__':
    main()