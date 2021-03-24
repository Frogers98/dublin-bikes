##------------------APP---------------##
## 
##User:     Disappster
##DC:       2021-03-01
##DLM:      2021-03-01
##MC:       COMP30830
##SD:       FLASK APP
##
##------------------APP---------------##



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
import sys
import os
import json
import time
import socket
import traceback as tb
import platform
import json
import pprint

######---------BEGIN
#     DATA VIS
######--------END

#import seaborn as sb
#import matplotlib as mp
#from bokeh import *
#from dash import *

#BeExplicit
from FlaskApp.data_dictionary import services_dictionary
from FlaskApp.data_dictionary import database_dictionary
from FlaskApp.data_dictionary import database_schema
from FlaskApp.sql import *

####--------------------------------------
#01. Connect to a Database Engine
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
                     ,1:'One of the parammeters is wrong'}
    
    try:
        connect_statement='mysql+mysqldb://{}:{}@{}:{}/{}'.format(user,password,host,port,db)
        print(connect_statement)
        engine=sqla.create_engine(connect_statement,echo=True)
        
    except:
        connect_statement='mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(user,password,host,port,db)
        print(connect_statement)
        engine=sqla.create_engine(connect_statement,echo=True)

    finally:
        print(connect_statement)
        engine=sqla.create_engine(connect_statement,echo=True)
        error_code=1
        error_message=error_dictionary[error_code]
        print(error_message)
        
    
    return [error_code,engine]



####--------------------------------------
#02. Setup the Database Schema and all related functions (e.g. foreign keys, primary keys)
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
#03. Get Stations
####--------------------------------------


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

def get_stations_json(host,user,password,port,db):
    """Returns the stations table as a json string
    The other functions can just call this instead of re-using the code in each function"""

    engine_l=connect_db_engine(host,user,password,port,db)
    engine=engine_l[1]

    print("in get_stations_json()")
    df = pd.read_sql_table("01_station", engine)
    station_json = df.to_json(orient="records")
    print("station data type:", type(station_json))
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint(station_json)
    print()
    return station_json

def requestStationData(host,user,password,port,db):
    """A function to Request Station Data and Output as Json"""

    engine_l=connect_db_engine(host,user,password,port,db)
    engine=engine_l[1]

    # Read sql database table into a dataframe
    df = pd.read_sql_table("01_station", engine)

    print(df.iloc[1])
    # Convert to JSON string
    stationJSON = df.to_json(orient="records")

    return stationJSON

def requestStationSQLAData(host,user,password,port,db):
    """A function to request Station Data using SQLAlchemy

    Returns Keys"""

    engine_l=connect_db_engine(host,user,password,port,db)
    engine=engine_l[1]

    metadata = sqla.MetaData()
    station_data = sqla.Table('01_station', metadata, autoload=True, autoload_with=engine)

    print(station_data.columns.keys())


####--------------------------------------
#04. Get Availability
####--------------------------------------


def availability_table_df(host,user,password,port,db):
    """Retrieve the station table.
    
    Return table as dataframe
    """
    
    print("Inside setup_database()\n\n")
    
    engine_l=connect_db_engine(host,user,password,port,db)
    engine=engine_l[1]
    df=pd.DataFrame()

    #no error
    try:
        df=pd.read_sql(SQL_select_availability,engine)
    
    except Exception as e:
        print(e)

    engine.dispose()

    return df

def availability_limit_df(host,user,password,port,db):
    """A function to pull the top 109 last updated availability stuff
    
    Returns a Json Dump of result
    """

    print("IN AVAILABILITY FUNCTION")

    engine_l=connect_db_engine(host,user,password,port,db)
    engine=engine_l[1]
    result = engine.execute(SQL_select_limit_availability)
    


    print("type of sql request is", type(result))

    for number, available_bikes, available_bike_stands, last_update, created_date in result:
        print("number is:", number, "available bikes is:", available_bikes, "available_bike_stands is:", available_bike_stands, "last update is:", last_update, "created date is:", created_date)
    
    #frontend=json.dumps(result)
    return 'Check JSON DUMPS'

def availability_recentUpdate(host,user,password,port,db):
    """Availability from SQL Alchemy Most recent Update limiting 109"""

    engine_l=connect_db_engine(host,user,password,port,db)
    engine=engine_l[1]

    try:
        engine.connect()

    except Exception as E:
        print(E)

    metadata = sqla.MetaData()
    availability_data = sqla.Table('01_availability', metadata, autoload=True, autoload_with=engine)
    query = sqla.select([availability_data]).order_by(sqla.desc(availability_data.columns.created_date)).limit(109)
    df = pd.read_sql_query(query, engine)
    print(df.iloc[:10])
    return df


####--------------------------------------
#05. Get Station and Availability Data
####--------------------------------------


def station_availability_df(host,user,password,port,db):
    """Retrieve the station table.
    
    Return table as dataframe
    """
    
    print("Inside setup_database()\n\n")
    
    engine_l=connect_db_engine(host,user,password,port,db)
    engine=engine_l[1]
    df=pd.DataFrame()

    #no error
    df=pd.read_sql(SQL_select_station_avail,engine)

    engine.dispose()

    return df

def station_availability_last_update_table_df(host,user,password,port,db):
    """Retrieve the station table.
    
    Return table as dataframe
    """
    
    print("Inside setup_database()\n\n")
    
    engine_l=connect_db_engine(host,user,password,port,db)
    engine=engine_l[1]
    df=pd.DataFrame()

    #no error
    try:
        df=pd.read_sql(SQL_select_station_avail_latest_update,engine)
    
    except Exception as e:
        print(e)

    engine.dispose()

    return df


####--------------------------------------
#06. Get Station and Availability And Weather Data
####--------------------------------------


def station_availability_weather_table_df(host,user,password,port,db):
    """Retrieve the station table.
    
    Return table as dataframe
    """
    
    print("Inside setup_database()\n\n")
    
    engine_l=connect_db_engine(host,user,password,port,db)
    engine=engine_l[1]
    df=pd.DataFrame()

    #no error
    df=pd.read_sql(SQL_select_station_avail_weather,engine)

    engine.dispose()

    return df

def station_availability_weather_table_latest_df(host,user,password,port,db):
    """Retrieve the station table.
    
    Return table as dataframe
    """
    
    print("Inside setup_database()\n\n")
    
    engine_l=connect_db_engine(host,user,password,port,db)
    engine=engine_l[1]
    df=pd.DataFrame()

    #no error
    df=pd.read_sql(SQL_select_avail_weather_conditional.format(SQL_select_availability_last_update,SQL_select_weather),engine)

    engine.dispose()

    return df