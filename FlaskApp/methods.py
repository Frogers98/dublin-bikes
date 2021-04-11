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

import nltk as nl
import sklearn as sk
import matplotlib as mp
import xgboost as xg
#import pymc3 as pymc
#import sympy as sym

from sklearn.model_selection import train_test_split, KFold, cross_val_score, GridSearchCV
from sklearn.metrics import mean_squared_error, accuracy_score, precision_score, recall_score



######---------BEGIN
#      SQL
######--------END


import requests
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
import pickle

######---------BEGIN
#     DATA VIS
######--------END

import seaborn as sns
import matplotlib as mp
#from bokeh import *
#from dash import *

import matplotlib.pyplot as plt

#BeExplicit
from data_dictionary import services_dictionary
from data_dictionary import ar_database_dictionary
from data_dictionary import database_schema
from sql import *





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
    engine.dispose()
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
    try:
        engine.dispose()
    except:
        df=pd.DataFrame()

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
    """This function pulls the station, weather, availability data.
    
    Note: This is very time intensive. Use this to pass to other summary functions"""
    
    print("Inside pull_station_weather_availability_data(host,user,password,port,db)")
    
    #Possible Errors
    error_dictionary={0:'No Error'
                     ,1:'The database failed to connect'
                     ,2:"The query is not a valid string"
                     ,3: "The returned database is empty"
                      ,999: 'Uncaught exception'
                     }
    
    #Set up a default value to return
    data_df=pd.DataFrame()
    
    error_code=0
    
    #Configure the SQL statement
    sql_statement=SQL_select_station_avail_weather
    
    time_statement="The retrieval from the database took: {} (ns)"
    
    #Begin try
    try:
        engine_l=connect_db_engine(host,user,password,port,db)
        engine=engine_l[1]
        
        #No error connecting to engine
        if engine_l[0]==0:
            
            #String
            if type(sql_statement)==str and len(sql_statement)>0:
                
                #Begin counter
                start_time=time.perf_counter_ns()
                data_df=pd.read_sql(sql_statement,engine)
                end_time=time.perf_counter_ns()
                engine.dispose()
                
                #Performance measurement
                print(time_statement.format(end_time-start_time))
                
                #Dataframe is empty
                if len(data_df)==0:
                    error_code=3
                    error_message=error_dictionary[error_code]
                    
            #Invalid SQL Statement
            else:
                error_code=2
                error_message=error_dictionary[error_code]         
        
        else:
            error_code=1
            error_message=error_dictionary[error_code]

    except Exception as e:
        error_code=999
        print("Unexpected failure: {}".format(e))
        
    return data_df


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

def availability_table_for_station_df(host,user,password,port,db,station_no):
    """Retrieve the station table.
    
    Return table as dataframe
    """
    
    print("Inside setup_database()\n\n")
    
    engine_l=connect_db_engine(host,user,password,port,db)
    engine=engine_l[1]
    df=pd.DataFrame()

    #no error
    try:
        df=pd.read_sql(SQL_select_availability_where_number.format(station_no),engine)
    
    except Exception as e:
        print(e)

    engine.dispose()

    return df


def weather_last_update_df(host, user, password, port, db):
    """Retrieve weather last update.

    Return table as dataframe
    """

    print("Inside setup_database()\n\n")

    engine_l = connect_db_engine(host, user, password, port, db)
    engine = engine_l[1]
    df = pd.DataFrame()

    # no error
    try:
        df = pd.read_sql(SQL_select_weather_last_update, engine)

    except Exception as e:
        print(e)

    engine.dispose()

    return df



####--------------------------------------
#07. Analytics function
####--------------------------------------



#-###-------------------------------------
#07.01 Functions for grouping by and aggregating
#-###-------------------------------------

def group_by_column(df,groupby_columns,agg_dict):
    """A function to group by columns given and aggregate according to a dictionary.
    
    Input: df, columns to group by, agg_dictionary
    """
    
    print("inside group_by_column(df,{},{})".format(groupby_columns,agg_dict))
    
    #Possible Errors
    error_dictionary={0:'No Error'
                     ,1:'The dataframe is empty'
                     ,2:"The columns to group by is empty or not a list"
                     ,3: 'The dictionary is empty'
                     ,4: 'The dataframe does not contain the required columns'
                      ,999: 'Uncaught exception'
                     }
    
    #Set as empty
    summary_df=pd.DataFrame()
    required_columns=[]
    
    error_code=0
    
    try:

        #Dictionary is non-empty
        if len(agg_dict)>0 and type(agg_dict)==dict:

            #df not empty
            if len(df)>0:

                #List and non-empty
                if type(groupby_columns)==list and len(groupby_columns)>0:
                    required_columns=list(df.columns)+list(agg_dict.keys())

                    #Required columns found
                    if set(required_columns).issubset(set(df.columns)):

                        #begin groupby - note: not catching summary issues as they are plentiful
                        summary_df=(df
                                        .groupby(groupby_columns)
                                        .agg(agg_dict)
                                        .reset_index()
                                    )


                    #Required columns not found    
                    else:
                        error_code=4
                        error_message=error_dictionary[error_code]
                        print(error_message)

                #Not a list or empty
                else:
                    error_code=2
                    error_message=error_dictionary[error_code]
                    print(error_message)

            #df is not empty
            else:
                error_code=1
                error_message=error_dictionary[error_code]
                print(error_message)

        #empty Dictionary
        else:
            error_code=3
            error_message=error_dictionary[error_code]
            print(error_message)
            
    except Exception as e:
        error_code=999
        print("Uncaught exception: {}".format(e))
        
    return [error_code,summary_df]
    

#-###-------------------------------------
#07.02 Functions for adding columns to dataframe
#-###-------------------------------------

def add_datestamp_to_dataframe(df,column_name):
    """Add datestamp of a column to a dataframe"""
    
    #Possible Errors
    error_dictionary={0:'No Error'
                     ,1:'The dataframe is empty'
                     ,2: 'The dataframe does not contain the required columns'
                      ,999: 'Uncaught exception'
                     }
    
    time_period_name='date'
    new_column_name='{}_{}'
    
    try:
    
        #dataframe not empty
        if len(df)>0:

            #column in df
            if column_name in df.columns:
                new_column_name=new_column_name.format(column_name,time_period_name)
                df[column_name]=pd.to_datetime(df[column_name])
                df[new_column_name]=df[column_name].dt.date

            #Column not in df
            else:
                error_code=2
                error_message=error_dictionary[error_code]
                print(error_message)

        #df empty
        else:
            error_code=1
            error_message=error_dictionary[error_code]
            print(error_message)
            
    except Exception as e:
        error_code=999
        error_message=error_dictionary[error_code]
        
    return df
    
    
def add_weekday_no_to_dataframe(df,column_name):
    """Add weekdayno of a column to a dataframe"""
    
    #Possible Errors
    error_dictionary={0:'No Error'
                     ,1:'The dataframe is empty'
                     ,2: 'The dataframe does not contain the required columns'
                      ,999: 'Uncaught exception'
                     }
    
    time_period_name='weekdayno'
    new_column_name='{}_{}'
    
    try:
    
        #dataframe not empty
        if len(df)>0:

            #column in df
            if column_name in df.columns:
                new_column_name=new_column_name.format(column_name,time_period_name)
                df[column_name]=pd.to_datetime(df[column_name])
                df[new_column_name]=df[column_name].dt.dayofweek

            #Column not in df
            else:
                error_code=2
                error_message=error_dictionary[error_code]
                print(error_message)

        #df empty
        else:
            error_code=1
            error_message=error_dictionary[error_code]
            print(error_message)
            
    except Exception as e:
        error_code=999
        error_message=error_dictionary[error_code]
        
    return df
    
def add_week_no_to_dataframe(df,column_name):
    """Add week no of a column to a dataframe"""
    
    #Possible Errors
    error_dictionary={0:'No Error'
                     ,1:'The dataframe is empty'
                     ,2: 'The dataframe does not contain the required columns'
                      ,999: 'Uncaught exception'
                     }
    
    time_period_name='weekno'
    new_column_name='{}_{}'
    
    try:
    
        #dataframe not empty
        if len(df)>0:

            #column in df
            if column_name in df.columns:
                new_column_name=new_column_name.format(column_name,time_period_name)
                df[column_name]=pd.to_datetime(df[column_name])
                df[new_column_name]=df[column_name].dt.week

            #Column not in df
            else:
                error_code=2
                error_message=error_dictionary[error_code]
                print(error_message)

        #df empty
        else:
            error_code=1
            error_message=error_dictionary[error_code]
            print(error_message)
            
    except Exception as e:
        error_code=999
        error_message=error_dictionary[error_code]
        
    
    return df
      
def add_month_no_to_dataframe(df,column_name):
    """Add month of a column to a dataframe"""
    
    #Possible Errors
    error_dictionary={0:'No Error'
                     ,1:'The dataframe is empty'
                     ,2: 'The dataframe does not contain the required columns'
                      ,999: 'Uncaught exception'
                     }
    
    time_period_name='monthno'
    new_column_name='{}_{}'
    
    try:
    
        #dataframe not empty
        if len(df)>0:

            #column in df
            if column_name in df.columns:
                new_column_name=new_column_name.format(column_name,time_period_name)
                df[column_name]=pd.to_datetime(df[column_name])
                df[new_column_name]=df[column_name].dt.month

            #Column not in df
            else:
                error_code=2
                error_message=error_dictionary[error_code]
                print(error_message)

        #df empty
        else:
            error_code=1
            error_message=error_dictionary[error_code]
            print(error_message)
            
    except Exception as e:
        error_code=999
        error_message=error_dictionary[error_code]
        
    return df

    
def add_hour_no_to_dataframe(df,column_name):
    """Add hour of a column to a dataframe"""
    
    #Possible Errors
    error_dictionary={0:'No Error'
                     ,1:'The dataframe is empty'
                     ,2: 'The dataframe does not contain the required columns'
                      ,999: 'Uncaught exception'
                     }
    
    time_period_name='hourno'
    new_column_name='{}_{}'
    
    try:
    
        #dataframe not empty
        if len(df)>0:

            #column in df
            if column_name in df.columns:
                new_column_name=new_column_name.format(column_name,time_period_name)
                df[column_name]=pd.to_datetime(df[column_name])
                df[new_column_name]=df[column_name].dt.hour

            #Column not in df
            else:
                error_code=2
                error_message=error_dictionary[error_code]
                print(error_message)

        #df empty
        else:
            error_code=1
            error_message=error_dictionary[error_code]
            print(error_message)
            
    except Exception as e:
        error_code=999
        error_message=error_dictionary[error_code]
        
    return df



#-###-------------------------------------
#07.03 Availability by timeperiod
#-###-------------------------------------

def avg_station_availability_by_weekdayno_df(host,user,password,port,db):
    """Returns the stations by weekdayno"""
    
    engine_l=connect_db_engine(host,user,password,port,db)
    engine=engine_l[1]
    ldf=pd.DataFrame()
    
    groupby_columns=[
                        'number'
                        ,'created_date_weekdayno'
                    ]
    
    column_name='created_date'
    
    agg_dict={
               'available_bikes':np.mean
              ,'available_bike_stands':np.mean
            }
    
    #Possible Errors
    error_dictionary={
                      0:'No Error'
                     ,1:'The database failed to connect'
                    ,999:'Uncaught Exception: '
                     }
    
    
    try:
        
        #No db error
        if engine_l[0]==0:
            
            #All availability data
            df=availability_table_df(host,user,password,port,db)
            
            #Staging Dataframe - Add time
            sdf=add_weekday_no_to_dataframe(df,column_name)
            
            #Load Dataframe
            ldf_l=group_by_column(sdf,groupby_columns,agg_dict)
    
            ldf=ldf_l[1]
            
       #db error 
        else:
            error_code=1
            error_message=error_dictionary[error_code]
            print(error_message)
            
        
    except Exception as E:
        error_code=999
        error_message=error_dictionary[error_code]
        print(error_message+E)
        
    return ldf

def avg_station_availability_by_monthno_df(host,user,password,port,db):
    """Returns the stations by date"""
    
    engine_l=connect_db_engine(host,user,password,port,db)
    engine=engine_l[1]
    ldf=pd.DataFrame()
    
    groupby_columns=[
                        'number'
                        ,'created_date_date'
                    ]
    
    column_name='created_date'
    
    agg_dict={
               'available_bikes':np.mean
              ,'available_bike_stands':np.mean
            }
    
    #Possible Errors
    error_dictionary={
                      0:'No Error'
                     ,1:'The database failed to connect'
                    ,999:'Uncaught Exception: '
                     }
    
    
    try:
        
        #No db error
        if engine_l[0]==0:
            
            #All availability data
            df=availability_table_df(host,user,password,port,db)
            
            #Staging Dataframe - Add time
            sdf=add_month_no_to_dataframe(df,column_name)
            
            #Load Dataframe
            ldf_l=group_by_column(sdf,groupby_columns,agg_dict)
    
            ldf=ldf_l[1]
            
       #db error 
        else:
            error_code=1
            error_message=error_dictionary[error_code]
            print(error_message)
            
        
    except Exception as E:
        error_code=999
        error_message=error_dictionary[error_code]
        print(error_message+E)
        
    return ldf

def avg_station_availability_by_weekno_df(host,user,password,port,db):
    """Returns the station no by weekno"""
    
    engine_l=connect_db_engine(host,user,password,port,db)
    engine=engine_l[1]
    ldf=pd.DataFrame()
    
    groupby_columns=[
                        'number'
                        ,'created_date_weekno'
                    ]
    
    column_name='created_date'
    
    agg_dict={
               'available_bikes':np.mean
              ,'available_bike_stands':np.mean
            }
    
    #Possible Errors
    error_dictionary={
                      0:'No Error'
                     ,1:'The database failed to connect'
                    ,999:'Uncaught Exception: '
                     }
    
    
    try:
        
        #No db error
        if engine_l[0]==0:
            
            #All availability data
            df=availability_table_df(host,user,password,port,db)
            
            #Staging Dataframe - Add time
            sdf=add_week_no_to_dataframe(df,column_name)
            
            #Load Dataframe
            ldf_l=group_by_column(sdf,groupby_columns,agg_dict)
    
            ldf=ldf_l[1]
            
       #db error 
        else:
            error_code=1
            error_message=error_dictionary[error_code]
            print(error_message)
            
        
    except Exception as E:
        error_code=999
        error_message=error_dictionary[error_code]
        print(error_message+E)
        
    return ldf

def avg_station_availability_by_date_df(host,user,password,port,db):
    """Returns the stations by date"""
    
    engine_l=connect_db_engine(host,user,password,port,db)
    engine=engine_l[1]
    ldf=pd.DataFrame()
    
    groupby_columns=[
                        'number'
                        ,'created_date_date'
                    ]
    
    column_name='created_date'
    
    agg_dict={
               'available_bikes':np.mean
              ,'available_bike_stands':np.mean
            }
    
    #Possible Errors
    error_dictionary={
                      0:'No Error'
                     ,1:'The database failed to connect'
                    ,999:'Uncaught Exception: '
                     }
    
    
    try:
        
        #No db error
        if engine_l[0]==0:
            
            #All availability data
            df=availability_table_df(host,user,password,port,db)
            
            #Staging Dataframe - Add time
            sdf=add_datestamp_to_dataframe(df,column_name)
            
            #Load Dataframe
            ldf_l=group_by_column(sdf,groupby_columns,agg_dict)
    
            ldf=ldf_l[1]
            
       #db error 
        else:
            error_code=1
            error_message=error_dictionary[error_code]
            print(error_message)
            
        
    except Exception as E:
        error_code=999
        error_message=error_dictionary[error_code]
        print(error_message+E)
        
    return ldf

def avg_station_availability_by_hourno_df(host,user,password,port,db):
    """Returns the stations by hour no"""
    
    engine_l=connect_db_engine(host,user,password,port,db)
    engine=engine_l[1]
    ldf=pd.DataFrame()
    
    groupby_columns=[
                        'number'
                        ,'created_date_hourno'
                    ]
    
    column_name='created_date'
    
    agg_dict={
               'available_bikes':np.mean
              ,'available_bike_stands':np.mean
            }
    
    #Possible Errors
    error_dictionary={
                      0:'No Error'
                     ,1:'The database failed to connect'
                    ,999:'Uncaught Exception: '
                     }
    
    
    try:
        
        #No db error
        if engine_l[0]==0:
            
            #All availability data
            df=availability_table_df(host,user,password,port,db)
            
            #Staging Dataframe - Add time
            sdf=add_hour_no_to_dataframe(df,column_name)
            
            #Load Dataframe
            ldf_l=group_by_column(sdf,groupby_columns,agg_dict)
    
            ldf=ldf_l[1]
            
       #db error 
        else:
            error_code=1
            error_message=error_dictionary[error_code]
            print(error_message)
            
        
    except Exception as E:
        error_code=999
        error_message=error_dictionary[error_code]
        print(error_message+E)
        
    return ldf

#-#-###-------------------------------------
#07.03.1 Availability by timeperiod for a particular station = Runs Faster via SQL WHERE 
#-#-###-------------------------------------


def avg_station_availability_by_weekdayno_df_forstat(host,user,password,port,db,station_no):
    """Returns the stations by weekdayno"""
    
    engine_l=connect_db_engine(host,user,password,port,db)
    engine=engine_l[1]
    ldf=pd.DataFrame()
    
    groupby_columns=[
                        'number'
                        ,'created_date_weekdayno'
                    ]
    
    column_name='created_date'
    
    agg_dict={
               'available_bikes':np.mean
              ,'available_bike_stands':np.mean
            }
    
    #Possible Errors
    error_dictionary={
                      0:'No Error'
                     ,1:'The database failed to connect'
                    ,999:'Uncaught Exception: '
                     }
    
    
    try:
        
        #No db error
        if engine_l[0]==0:
            
            #All availability data
            df=availability_table_for_station_df(host,user,password,port,db,station_no)
            
            #Staging Dataframe - Add time
            sdf=add_weekday_no_to_dataframe(df,column_name)
            
            #Load Dataframe
            ldf_l=group_by_column(sdf,groupby_columns,agg_dict)
    
            ldf=ldf_l[1]
            
       #db error 
        else:
            error_code=1
            error_message=error_dictionary[error_code]
            print(error_message)
            
        
    except Exception as E:
        error_code=999
        error_message=error_dictionary[error_code]
        print(error_message+E)
        
    return ldf

def avg_station_availability_by_monthno_df_forstat(host,user,password,port,db,station_no):
    """Returns the stations by date"""
    
    engine_l=connect_db_engine(host,user,password,port,db)
    engine=engine_l[1]
    ldf=pd.DataFrame()
    
    groupby_columns=[
                        'number'
                        ,'created_date_date'
                    ]
    
    column_name='created_date'
    
    agg_dict={
               'available_bikes':np.mean
              ,'available_bike_stands':np.mean
            }
    
    #Possible Errors
    error_dictionary={
                      0:'No Error'
                     ,1:'The database failed to connect'
                    ,999:'Uncaught Exception: '
                     }
    
    
    try:
        
        #No db error
        if engine_l[0]==0:
            
            #All availability data
            df=availability_table_for_station_df(host,user,password,port,db,station_no)
            
            #Staging Dataframe - Add time
            sdf=add_month_no_to_dataframe(df,column_name)
            
            #Load Dataframe
            ldf_l=group_by_column(sdf,groupby_columns,agg_dict)
    
            ldf=ldf_l[1]
            
       #db error 
        else:
            error_code=1
            error_message=error_dictionary[error_code]
            print(error_message)
            
        
    except Exception as E:
        error_code=999
        error_message=error_dictionary[error_code]
        print(error_message+E)
        
    return ldf

def avg_station_availability_by_weekno_df_forstat(host,user,password,port,db,station_no):
    """Returns the station no by weekno"""
    
    engine_l=connect_db_engine(host,user,password,port,db)
    engine=engine_l[1]
    ldf=pd.DataFrame()
    
    groupby_columns=[
                        'number'
                        ,'created_date_weekno'
                    ]
    
    column_name='created_date'
    
    agg_dict={
               'available_bikes':np.mean
              ,'available_bike_stands':np.mean
            }
    
    #Possible Errors
    error_dictionary={
                      0:'No Error'
                     ,1:'The database failed to connect'
                    ,999:'Uncaught Exception: '
                     }
    
    
    try:
        
        #No db error
        if engine_l[0]==0:
            
            #All availability data
            df=availability_table_for_station_df(host,user,password,port,db,station_no)
            
            #Staging Dataframe - Add time
            sdf=add_week_no_to_dataframe(df,column_name)
            
            #Load Dataframe
            ldf_l=group_by_column(sdf,groupby_columns,agg_dict)
    
            ldf=ldf_l[1]
            
       #db error 
        else:
            error_code=1
            error_message=error_dictionary[error_code]
            print(error_message)
            
        
    except Exception as E:
        error_code=999
        error_message=error_dictionary[error_code]
        print(error_message+E)
        
    return ldf

def avg_station_availability_by_date_df_forstat(host,user,password,port,db,station_no):
    """Returns the stations by date"""
    
    engine_l=connect_db_engine(host,user,password,port,db)
    engine=engine_l[1]
    ldf=pd.DataFrame()
    
    groupby_columns=[
                        'number'
                        ,'created_date_date'
                    ]
    
    column_name='created_date'
    
    agg_dict={
               'available_bikes':np.mean
              ,'available_bike_stands':np.mean
            }
    
    #Possible Errors
    error_dictionary={
                      0:'No Error'
                     ,1:'The database failed to connect'
                    ,999:'Uncaught Exception: '
                     }
    
    
    try:
        
        #No db error
        if engine_l[0]==0:
            
            #All availability data
            df=availability_table_for_station_df(host,user,password,port,db,station_no)
            
            #Staging Dataframe - Add time
            sdf=add_datestamp_to_dataframe(df,column_name)
            
            #Load Dataframe
            ldf_l=group_by_column(sdf,groupby_columns,agg_dict)
    
            ldf=ldf_l[1]
            
       #db error 
        else:
            error_code=1
            error_message=error_dictionary[error_code]
            print(error_message)
            
        
    except Exception as E:
        error_code=999
        error_message=error_dictionary[error_code]
        print(error_message+E)
        
    return ldf

def avg_station_availability_by_hourno_df_forstat(host,user,password,port,db,station_no):
    """Returns the stations by hour no"""
    
    engine_l=connect_db_engine(host,user,password,port,db)
    engine=engine_l[1]
    ldf=pd.DataFrame()
    
    groupby_columns=[
                        'number'
                        ,'created_date_hourno'
                    ]
    
    column_name='created_date'
    
    agg_dict={
               'available_bikes':np.mean
              ,'available_bike_stands':np.mean
            }
    
    #Possible Errors
    error_dictionary={
                      0:'No Error'
                     ,1:'The database failed to connect'
                    ,999:'Uncaught Exception: '
                     }
    
    
    try:
        
        #No db error
        if engine_l[0]==0:
            
            #All availability data
            df=availability_table_for_station_df(host,user,password,port,db,station_no)
            
            #Staging Dataframe - Add time
            sdf=add_hour_no_to_dataframe(df,column_name)
            
            #Load Dataframe
            ldf_l=group_by_column(sdf,groupby_columns,agg_dict)
    
            ldf=ldf_l[1]
            
       #db error 
        else:
            error_code=1
            error_message=error_dictionary[error_code]
            print(error_message)
            
        
    except Exception as E:
        error_code=999
        error_message=error_dictionary[error_code]
        print(error_message+E)
        
    return ldf



#-#-###-------------------------------------
#08 Model Functions
#-#-###-------------------------------------

def add_time_features(df, date_time_column):
    """
    Various time features for analytics
    """
    print(df)
    #Features to keep
    #df['timestamp']=(df[date_time_column].astype(int)/10**9).astype(int)
    df['hour'] = df[date_time_column].dt.hour
    df['dayofweek'] = df[date_time_column].dt.dayofweek
    df['dayofmonth'] = df[date_time_column].dt.day
    df['dayofyear'] = df[date_time_column].dt.dayofyear
    
    df['bool_weekend']=np.where(df['dayofweek']>4, True, False)
    #df['bool_level5']=np.where(df['dayofyear']<pd.to_datetime('2021-05-04').dt.day, True, False)
    
    #Bank Holidays and weekend
    df['bool_dayoff']=False
    
    df.loc[(df['dayofweek']>4) |
       (df['dayofyear']==pd.to_datetime('2021-03-17').dayofyear) | 
       (df['dayofyear']==pd.to_datetime('2021-04-05').dayofyear) | 
        (df['dayofyear']==pd.to_datetime('2021-05-04').dayofyear),
       'bool_dayoff'] = True
    
    #Work Hours 9am to 5pm
    df['bool_workhour']=True
    df.loc[(df['hour']>8) &
            (df['hour']<16),'bool_workhour']=False
    
    df.loc[(df['dayofweek']>4) |
       ((df['dayofyear']==pd.to_datetime('2021-03-17').dayofyear) |
       (df['dayofyear']==pd.to_datetime('2021-04-05').dayofyear) |
        (df['dayofyear']==pd.to_datetime('2021-05-04').dayofyear)),
       'bool_dayoff'] = True   
    
    df['bool_commutehour']=False
    df.loc[((df['hour']>=7) & (df['hour']<=8)) |
           ((df['hour']>=16) & (df['hour']<=17)),'bool_commutehour']= True
       
    #9pm - 5am
    df['bool_night']=False
    df.loc[(df['hour']>20) | 
            (df['hour']<6),'bool_night']=True
                        
    #Poor Results:
    #df['quarter'] = df[date_time_column].dt.quarter
    #df['month'] = df[date_time_column].dt.month
    #df['year'] = df[date_time_column].dt.year
    #df['minute'] = df[date_time_column].dt.minute
    #df['weekofyear'] = df[date_time_column].dt.weekofyear
    #df=d#f.drop(date_time_column, axis=1)

    df=df.drop('dayofyear',axis=1)
    
    return [df,['hour','dayofweek','dayofmonth','bool_weekend','bool_dayoff','bool_workhour','bool_commutehour','bool_night']]


def get_randomised_data(host,user,password,port,db,df,test_size=0.3):
    """Function to split the dataframe randomly into testing and training data and store these sets as tables in the db"""
    #print(df.head(5))
    # Splits the dataset into training and testing sets
    # 70% training data, 30$ testing data
    print("about to split into train and test")
    
    engine_l=connect_db_engine(host,user,password,port,db)
    engine=engine_l[1]

    train, test = train_test_split(df, test_size=test_size)
    print("finished loading train and test dataframes")

    train.to_sql(name='02_availability_train', con=engine, if_exists='replace', index=False)
    print("finished loading data into 02_availability_train")
    test.to_sql(name='02_availability_test', con=engine, if_exists='replace', index=False)
    print("finished loading data into 02_availability_test")
    return

def get_test_date(df,time_column,test_set_size=0.2, verbose=False):
    """A function to determine what date should be our test date"""
    
    #Default Date
    datetime_at_test_limit=pd.to_datetime('2020-04-01')

    sorted_datetimes=df[time_column].sort_values().unique()

    number_of_datetimes=len(sorted_datetimes)
    print("Total dates: {}".format(number_of_datetimes))

    number_of_test_dates=test_set_size*number_of_datetimes
    print("Test dates: {}".format(number_of_test_dates))

    test_index=int(number_of_datetimes - number_of_test_dates)
    print("Test index: {}".format(test_index))

    datetime_at_test_limit=sorted_datetimes[test_index]
    
    if verbose:
        print("Total dates: {}".format(number_of_datetimes))
        print("Test dates: {}".format(number_of_test_dates))
        print("Test index: {}".format(test_index))
        print("Dates after {} are test dates".format(datetime_at_test_limit))
        


    return datetime_at_test_limit

def create_xgboost_model(fulldf,train_df,test_df,target_column,station_number,plot_comp,plot_tree):
    """Create an xgboostmodel"""
    
    X=fulldf.drop([target_column], axis=1)
    y=fulldf[target_column]
    
    X_test=test_df.drop([target_column], axis=1)
    y_test= test_df[target_column]
    
    X_train=train_df.drop([target_column], axis=1)
    y_train=train_df[target_column]
    
    
    #Paramter Dictionary
    
    model_parameters = {'nthread':[4], #when use hyperthread, xgboost may become slower
              'objective':['reg:squarederror'],
              'learning_rate': [.03, 0.05, .07], #so called `eta` value
              'max_depth': [5, 6, 7,8],
              'min_child_weight': [4],
              'subsample': [0.7],
              'colsample_bytree': [0.7],
              'n_estimators': [500]}

    #Create the XGBoost Regresspr
    xg_regression_model = xg.XGBRegressor(objective ='reg:squarederror')
    
    #Hypertune
    grid = GridSearchCV(xg_regression_model, model_parameters)
    grid.fit(X_train, y_train)
    
    best_parameters=grid.best_params_
    xg_regression_model = grid.best_estimator_


    #Score the model
    score=xg_regression_model.score(X_train,y_train)
    print("Model Training Score: {}%".format(score*100))
    
    #Check the predictions
    model_prediction = xg_regression_model.predict(X_test)
    
    kfold = KFold(n_splits=10)
    results = cross_val_score(xg_regression_model, X, y, cv=kfold)
    print("Model Accuracy: {}".format(results * 100))
    
    if plot_comp:
        #Original Versus Prediction
        print("The Original Vs Predicted Result Is:")
        plt.figure(figsize=(50,20)) 
        x_axis = range(len(y_test))
        plt.plot(x_axis, y_test, label="Original")
        plt.plot(x_axis, model_prediction, label="Predicted")
        plt.title("Station test and predicted data")
        plt.legend()
        plt.savefig('xg_pred_vs_orig_{}.png'.format(station_number))
        plt.show()
    
    
    filename = './xg_model_station_{}.pickle'
    pickle.dump(xg_regression_model, open(filename.format(station_number), 'wb'))
    
    pred_vs_act_df=pd.DataFrame({'Actual':y_test,'Predicted':model_prediction})
    pred_vs_act_df['Predicted']=pred_vs_act_df['Predicted'].astype(int)
    pred_vs_act_df['Diff']=pred_vs_act_df['Actual']-pred_vs_act_df['Predicted']
    rmse=np.sqrt(mean_squared_error(y_test, model_prediction))
    print("RMSE: {}" .format(np.sqrt(mean_squared_error(y_test, model_prediction))))
    
    
    if plot_tree:
        #Visualisations, sometimes not great
        try:        

            #Tree Plot
            print("The Tree Is:")
            fig, ax = plt.subplots(figsize=(50, 20))
            xg.plot_tree(xg_regression_model,num_trees=2,ax=ax)
            plt.savefig('xg_tree_{}.png'.format(station_number))
            plt.show()

        
        
        
        except Exception as e:
            print(e)
        
    return [xg_regression_model,score,results,pred_vs_act_df,rmse]


def create_linear_model(fulldf,train_df,test_df,target_column,station_number,plot_comp):
    """Create a linear model"""
    
    X=fulldf.drop([target_column], axis=1)
    y=fulldf[target_column]
    
    X_test=test_df.drop([target_column], axis=1)
    y_test= test_df[target_column]
    
    X_train=train_df.drop([target_column], axis=1)
    y_train=train_df[target_column]
    
    
    #Paramter Dictionary


    #Create the XGBoost Regresspr
    lin_regression_model = sk.linear_model.LinearRegression()


    #Fit the data
    lin_regression_model.fit(X_train,y_train)
    
    #Check the predictions
    lin_prediction = lin_regression_model.predict(X_test)
    
    if plot_comp:
        #Original Versus Prediction
        print("The Original Vs Predicted Result Is:")
        plt.figure(figsize=(50,20)) 
        x_axis = range(len(y_test))
        plt.plot(x_axis, y_test, label="Original")
        plt.plot(x_axis, lin_prediction, label="Predicted")
        plt.title("Station test and predicted data")
        plt.legend()
        plt.savefig('lin_pred_vs_orig_{}.png'.format(station_number))
        plt.show()
    
    filename = './lin_model_station_{}.pickle'
    pickle.dump(lin_regression_model, open(filename.format(station_number), 'wb'))
    
    pred_vs_act_df=pd.DataFrame({'Actual':y_test,'Predicted':lin_prediction})
    pred_vs_act_df['Predicted']=pred_vs_act_df['Predicted'].astype(int)
    pred_vs_act_df['Diff']=pred_vs_act_df['Actual']-pred_vs_act_df['Predicted']
    rmse=np.sqrt(mean_squared_error(y_test, lin_prediction))
    print("RMSE: {}" .format(np.sqrt(mean_squared_error(y_test,lin_prediction))))
        
    return [lin_regression_model,'','',pred_vs_act_df,rmse]

###ADD IN SAVE TO TEST/TRAIN DB HERE
def generate_models(raw_df,host,user,password,port,db, plot_comp=True,plot_tree=True):
    """A function to generate models per station"""
        
    engine_l=connect_db_engine(host,user,password,port,db)
    engine=engine_l[1]

    try:
        #Try Clear the DB
        engine.execute("""DELETE FROM 02_station_avail_weather_train WHERE 1=1""")
        engine.execute("""DELETE FROM 02_station_avail_weather_test WHERE 1=1""")
    except:
        print('Cannot Remove')

    #HardCoded inputs - NOT A GOOD PRACTICE
    
    #Update time column
    update_time_column='entry_create_date'
    
    #Cleansed Columns
    cleansed_column_mapping={
                            'number': ['station_number']
                         , 'address': ['station_address']
                         , 'banking': ['station_banking']
                         , 'bike_status': ['station_bike_status']
                         , 'bike_stands': ['station_bike_stands']
                         ,  'contract_name': ['contract_name']
                         , 'name': ['station_name']
                         , 'position_lat': ['station_position_lat']
                         , 'position_long': ['station_position_lat']
                         ,  'available_bikes':['available_bikes']
                         , 'available_bike_stands':['available_bike_stands']
                         , 'last_update':['stand_last_update']
                         , 'created_date':[update_time_column]
                         , 'weather_position_long':['weather_position_long']
                         , 'weather_position_lat':['weather_position_lat']
                         ,  'weather_id':['weather_type_id']
                         , 'main':['weather_type_main']
                         , 'description':['weather_type_detail']
                         , 'icon':['weather_icon_type']
                         , 'icon_url':['weather_icon_url']
                         , 'base':['weather_base_name']
                         , 'temp':['weather_temp']
                         , 'feels_like':['weather_temp_feels_like']
                         , 'temp_min':['weather_temp_min']
                         , 'temp_max':['weather_temp_max']
                         , 'pressure':['weather_air_pressure']
                         , 'humidity':['weather_humidity']
                         , 'visibility':['weather_visibility']
                         , 'wind_speed':['weather_wind_speed']
                         , 'wind_degree':['weather_wind_direction']
                         , 'clouds_all':['clouds']
                         , 'datetime':['weather_datetime']
                         , 'sys_id':['weather_system_id']
                         , 'sys_country':['weather_country']
                         , 'sys_sunrise':['weather_sunrise_time']
                         , 'sys_sunset':['weather_sunrise_time']
                         , 'sys_type':['weather_station_type']
                         , 'timezone':['weather_timezone']
                         , 'id':['weather_pk']
                         , 'weather_name':['weather_place_name']
                         , 'cod':['weather_code']
                         }
    
    
    #Features - Initial
    relevant_feature_columns={
                    'feature':[
                                'station_number'
                               ,update_time_column
                               ,'weather_type_id'
                               ,'weather_temp'
                               ,'weather_temp_feels_like'
                               ,'weather_air_pressure'
                               ,'weather_humidity'
                              ]
    
                    ,'target':[
                                'available_bikes'
                              ]
                    
                            }
    
    
    

    #Staging Dataframe
    staging_df=raw_df.copy(deep=True)
    
    
    ###------
    #Rename Columns to Verbose - This should be functionised
    column_mapping={}
    
    for key,value in cleansed_column_mapping.items():
        for v in value:
            column_mapping[key] =  v

    
    staging_df=staging_df.rename(columns=column_mapping)
    
    #Column Renaming complete
    ###------
    
    
    
    ###------
    #Drop irrelevant features - This should be functionised
    keep_columns=[]

    for value in relevant_feature_columns.values():
        keep_columns+=value

    keep_columns=list(set(keep_columns))
    ###------
    
    
    ###------
    #Object column conversion to category for xgboost
    for object_column in ['station_number']:#,'weather_type_id']:
        
        #Check if in column list
        if object_column in staging_df.columns:
            
            #Change to category
            staging_df[object_column]=staging_df[object_column].astype('category')
            
        #Not in column list
        else:
            print("Missing {}".format(object_column))

    ###------
    staging_df=staging_df[keep_columns]
    
    #Add on day, hour, week
    time_feature_list=add_time_features(df=staging_df, date_time_column=update_time_column)
    
    #Staging Data with time features added
    staging_df=time_feature_list[0]
    
    #List of the time features added
    time_columns=time_feature_list[1]
    
    #Test Date Cutoff
    test_date=get_test_date(df=staging_df,time_column=update_time_column, test_set_size=0.2, verbose=False)

    #Get the average per hour - e.g. 5 10 stations, 1 0 station - avg is 50/6
    
    groupby_columns=[]
    
    for feature in relevant_feature_columns['feature']:
        if feature not in [update_time_column, 'station_number','weather_temp_feels_like','weather_temp','weather_humidity','weather_air_pressure']:
            groupby_columns+=[feature]
            
    for time_feature in time_columns:
        groupby_columns+=[time_feature]
    
    
    aggregation_dictionary={relevant_feature_columns['target'][0] : np.nanmean
                           ,'weather_temp_feels_like' : np.nanmean
                           ,'weather_temp' : np.nanmean
                           ,'weather_humidity' : np.nanmean
                           ,'weather_air_pressure' : np.nanmean
                           }
    
    print(time_columns)
    print(groupby_columns)
    print(aggregation_dictionary)
    
    
    station_dataframe_model_list={}
    datetime_now=dt.datetime.now()
    created_date=dt.datetime.timestamp(datetime_now)

    #For each station in the list
    for station_number in staging_df['station_number'].sort_values().unique():
        print("---------------")
        print("---------------")
        print("STATION {}".format(station_number))
        
        station_dataframe=pd.DataFrame()
        
            
        #Filter adf to that Dataframe
        station_dataframe=staging_df[staging_df['station_number']==station_number]
        
        #Station dataframe non-empty
        if len(station_dataframe)>0 and station_number!=507 and station_number!=508 and station_number!=509 and station_number!='507' and station_number!='508' and station_number!='509':
            
            #Drop feature of cardinality 1
            if 'station_number' in station_dataframe.columns:
                station_dataframe=station_dataframe.drop('station_number',axis=1)
                
            #Create Training and Test Split
            station_train_df=station_dataframe[station_dataframe[update_time_column] < test_date]
            station_test_df=station_dataframe[station_dataframe[update_time_column] >= test_date]
            
            
            station_dataframe=station_dataframe.drop(update_time_column,axis=1)
            station_train_df=station_train_df.drop(update_time_column,axis=1)
            station_test_df=station_test_df.drop(update_time_column,axis=1)
            
            #Need to do this here for filtering by date - will cause a slight imbalance in size via agg
            station_dataframe=(station_dataframe
                     .groupby(groupby_columns)
                     .agg(aggregation_dictionary)
                     .reset_index()
                    .dropna()
                )            
            
            #Need to do this here for filtering by date - will cause a slight imbalance in size via agg
            station_train_df=(station_train_df
                     .groupby(groupby_columns)
                     .agg(aggregation_dictionary)
                     .reset_index()
                    .dropna()
                )
            
            
            #Need to do this here for filtering by date - will cause a slight imbalance in size via agg
            station_test_df=(station_test_df
                     .groupby(groupby_columns)
                     .agg(aggregation_dictionary)
                     .reset_index()
                    .dropna()
                )
            

            #This won't work - It needs to be a function 
            try:
                #Don't touch the actual data
                temp_train_df=station_train_df.copy(deep=True)
                temp_test_df=station_test_df.copy(deep=True)

                #Add on created column
                temp_train_df['created_date']=created_date
                temp_test_df['created_date']=created_date

                #Station Number
                temp_train_df['number']=station_number
                temp_test_df['number']=station_number

                #Test/Train to DB
                temp_train_df.to_sql(name='02_station_avail_weather_train', con=engine, if_exists='append', index=False)
                temp_test_df.to_sql(name='02_station_avail_weather_test', con=engine, if_exists='append', index=False)
            
                #Remove these from memory
                del temp_train_df
                del temp_test_df

            except Exception as e:
                print("Exception posting testing and training data: {}".format(e))
                
            #One hot encoding of Weather Type
            #station_dataframe=pd.get_dummies(station_dataframe, drop_first=True)
            #station_train_df=pd.get_dummies(station_train_df, drop_first=True)
            #station_test_df=pd.get_dummies(station_test_df, drop_first=True)
            
            
            #Get station model
            model_result=create_xgboost_model(fulldf=station_dataframe,train_df=station_train_df,test_df=station_test_df,target_column='available_bikes',station_number=station_number,plot_comp=plot_comp,plot_tree=plot_tree)
            lin_model_result=create_linear_model(fulldf=station_dataframe,train_df=station_train_df,test_df=station_test_df,target_column='available_bikes',station_number=station_number,plot_comp=plot_comp)
                        
            #Get list of results to nester dict - Hefty RAM wise
            station_dataframe_model_list[station_number]={'model':model_result[0]
                                                         ,'score':model_result[1]
                                                         ,'results':model_result[2]
                                                         ,'predicted_vs_actual':model_result[3]
                                                         ,'rmse':model_result[4]
                                                        ,'lin_model':lin_model_result[0]
                                                         ,'lin_score':lin_model_result[1]
                                                         ,'lin_results':lin_model_result[2]
                                                         ,'lin_predicted_vs_actual':lin_model_result[3]
                                                         ,'lin_rmse':lin_model_result[4]
                                                         }
        
        #Pass Station
        else:
            print("No Data: {}".format(station_number))

    engine.dispose()        
    
    return station_dataframe_model_list


def wrap_generate_models(host,user,password,port,db, plot_comp=False,plot_tree=False):
    """A function to run the model generation"""

    raw_df=station_availability_weather_table_df(host,user,password,port,db)  
    model_data=generate_models(raw_df,host,user,password,port,db,plot_comp=False,plot_tree=False)

    return model_data





###-------------------------------------
#09 Forecast Functions - Previously separate file
###-------------------------------------

def get_forecast_for_time(host,user,password,port,db,station_no,timestamp):
    """This function pulls the station, weather, availability data.
    
    Note: This is very time intensive. Use this to pass to other summary functions"""
    
    print("Inside pull_station_weather_availability_data(host,user,password,port,db)")
    
    #Possible Errors
    error_dictionary={0:'No Error'
                     ,1:'The database failed to connect'
                     ,2:"The query is not a valid string"
                     ,3: "The returned database is empty"
                      ,999: 'Uncaught exception'
                     }
    
    #Set up a default value to return
    data_df=pd.DataFrame()
    
    error_code=0
    
    #Configure the SQL statement
    sql_statement=SQL_select_forecast_where_station_and_time.format(station_no,timestamp)
    
    time_statement="The retrieval from the database took: {} (ns)"
    
    #Begin try
    try:
        engine_l=connect_db_engine(host,user,password,port,db)
        engine=engine_l[1]
        
        #No error connecting to engine
        if engine_l[0]==0:
            
            #String
            if type(sql_statement)==str and len(sql_statement)>0:
                
                #Begin counter
                start_time=time.perf_counter_ns()
                data_df=pd.read_sql(sql_statement,engine)
                end_time=time.perf_counter_ns()
                engine.dispose()
                
                #Performance measurement
                print(time_statement.format(end_time-start_time))
                
                #Dataframe is empty
                if len(data_df)==0:
                    error_code=3
                    error_message=error_dictionary[error_code]
                    
            #Invalid SQL Statement
            else:
                error_code=2
                error_message=error_dictionary[error_code]         
        
        else:
            error_code=1
            error_message=error_dictionary[error_code]

    except Exception as e:
        error_code=999
        print("Unexpected failure: {}".format(e))
        
    return data_df




def getWeatherForecast(latitude, longitude):
    """Function to return the weather forecast for certain co-ordinates"""
    weather_key = services_dictionary['OpenWeatherMapForecast']['API Key']
    endpoint=services_dictionary['OpenWeatherMapForecast']['Endpoint']['weather_at_coord']
    r = requests.get(endpoint, params={"APPID": weather_key, "lat": latitude, "lon": longitude})
    return r.json()



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

def predict_from_station_time(weather_data,station_number,timestamp):
    """A function to predict from a station number and timestamp"""

    #Columns from Weather Query
    weather_columns=['number'
                    ,'weather_id'
                    ,'main'
                    ,'description'
                    ,'temp'
                    ,'feels_like'
                    ,'temp_min'
                    ,'temp_max'
                    ,'pressure'
                    ,'humidity'
                    ,'visibility'
                    ,'wind_speed'
                    ,'wind_degree'
                    ,'clouds_all'
                    ,'forecast_time_dt'
                    ,'weather_time']

    prediction_datetime=pd.to_datetime(timestamp)



    cleansed_column_mapping={
                            'number': ['station_number']
                         ,  'weather_id':['weather_type_id']
                         , 'main':['weather_type_main']
                         , 'description':['weather_type_detail']
                         , 'temp':['weather_temp']
                         , 'feels_like':['weather_temp_feels_like']
                         , 'temp_min':['weather_temp_min']
                         , 'temp_max':['weather_temp_max']
                         , 'pressure':['weather_air_pressure']
                         , 'humidity':['weather_humidity']
                         , 'visibility':['weather_visibility']
                         , 'wind_speed':['weather_wind_speed']
                         , 'wind_degree':['weather_wind_direction']
                         , 'clouds_all':['clouds']
                         , 'forecast_time_dt':['weather_datetime']
                         ,'weather_time':['weather_time']
                         }
    
    update_time_column='weather_datetime'

    #Features - Initial
    relevant_feature_columns={
                    'feature':[
                                'station_number'
                               ,update_time_column
                               ,'weather_type_id'
                               ,'weather_temp'
                               ,'weather_temp_feels_like'
                               ,'weather_air_pressure'
                               ,'weather_humidity'
                              ]
                    
                            }

    #Staging Dataframe
    staging_df=weather_data.copy(deep=True)
    
    
    ###------
    #Rename Columns to Verbose - This should be functionised
    column_mapping={}
    
    for key,value in cleansed_column_mapping.items():
        for v in value:
            column_mapping[key] =  v

    
    staging_df=staging_df.rename(columns=column_mapping)

    
    #Column Renaming complete
    ###------
    
    
    
    ###------
    #Drop irrelevant features - This should be functionised
    keep_columns=[]

    for value in relevant_feature_columns.values():
        keep_columns+=value

    keep_columns=list(set(keep_columns))
    ###------
    
    
    ###------
    #Object column conversion to category for xgboost
    for object_column in ['station_number']:#,'weather_type_id']:
        
        #Check if in column list
        if object_column in staging_df.columns:
            
            #Change to category
            staging_df[object_column]=staging_df[object_column].astype('category')
            
        #Not in column list
        else:
            print("Missing {}".format(object_column))

    ###------
    staging_df=staging_df[keep_columns]

    print(staging_df.describe())
    
    #Add on day, hour, week
    time_feature_list=add_time_features(df=staging_df, date_time_column=update_time_column)
    
    #Staging Data with time features added
    staging_df=time_feature_list[0]

    staging_df=staging_df.drop(update_time_column,axis=1)
    staging_df=staging_df.drop('station_number',axis=1)

    print(staging_df.dtypes)

    staging_df=staging_df[['weather_type_id',
 'hour',
 'dayofweek',
 'dayofmonth',
 'bool_weekend',
 'bool_dayoff',
 'bool_workhour',
 'bool_commutehour',
 'bool_night',
 'weather_temp_feels_like',
 'weather_temp',
 'weather_humidity',
 'weather_air_pressure']]

    #Had to swap to linear model as XGBoost is not loading due to save
    loaded_model = pickle.load(open('./predictive_models/lin_model_station_{}.pickle'.format(station_number), 'rb'))
    print(staging_df.columns)
    result = loaded_model.predict(staging_df)
    
    return result
