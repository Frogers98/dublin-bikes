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
                                ,'sys_type':'INT'
                                ,'sys_id':'INT'
                                ,'sys_message':'REAL'
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
               }

######---------BEGIN
#     DATA VIS
######--------END

#import seaborn as sb
#import matplotlib as mp
#from bokeh import *
#from dash import *


####--------------------------------------
#01. Dictionary
####--------------------------------------


####--------------------------------------
#02. Pull from Dublin Bike API
####--------------------------------------

def request_dublinbike_data():
    """Request Dublin Bike Data.
    
    Inpu: Key
    Output: JsonTEXT
    """
    print("Inside request_dublinbike_data()\n\n")
    dbikes_endpoint=services_dictionary['Dublin Bikes']['Endpoint']['Station']
    dbikes_key=services_dictionary['Dublin Bikes']['API Key']
    dbikes_contract='dublin'
    
    #Error handling
    error_dictionary={
                         0:'Success'
                        ,1:'There was an error in the request'
                        }
    
    #Assume no error by default
    error_code=0
    
    #Attempt the Request
    try:
        request_response=rq.get(dbikes_endpoint,params={"apiKey":dbikes_key,
                                                 "contract":dbikes_contract})
        
        json_text=request_response.json()
        
    #Failed for some reason
    except:
        error_code=1
        error_message=error_dictionary[error_code]
        json_text=''
        json_response=''
        
        print(error_message)
        
    return [error_code,json_text]    


####--------------------------------------
#03. Write Some Text to File if Needed
####--------------------------------------

def write_to_file(filepath,filename,text):
    """Write text to a file of your name
    
    filepath=Path of File e.g C://user//test
    filename=Name of File. No Extension
    text=text to write
    
    Output: [error,fp]
    """
    
    #Static
    datetime_now=dt.datetime.now()
    timestamp_format=dt.datetime.timestamp(datetime_now)
    fn='{}_{}'.format(filename,timestamp_format)
    fp='{}/{}.txt'.format(filepath,fn)
    
    
    #Error handling
    error_dictionary={
                        0:'Success'
                        ,1:'The filepath does not exist. You entered:\n{}'
                        ,2:'There was an error writing to text.'
                        }
    
    #Assume no error by default
    error_code=0
    
    
    #Check that the filepath exists
    if os.path.exists(filepath) or (filepath=='' or filepath=='.'):
        
        
        #open the file
        with open(fp, 'w') as f:
            print('Writing to: \n{}\n\n'.format(fp))
            
            #Try Write
            try:
                print('File Written')
                f.write(text)
                
                
            #Write Error
            except:
                error_code=2
                error_message=error_dictionary[error_code].format(filepath)
                print(error_message)
        
    #File path does not exist
    else:
        error_code=1
        error_message=error_dictionary[error_code].format(filepath)
        print(error_message)
        
    return [error_code,fp]




####--------------------------------------
#04. Flatten Dublin Bikes and Write it to File. More specific version of 3.
####--------------------------------------


def write_flatten_dublinbikes_to_text(filepath,json):
    """Write text to a file of your name
    
    filepath=Path of File e.g C://user//test
    filename=Name of File. No Extension
    text=text to write
    
    output: [error,fp]
    """
    
    #Static
    datetime_now=dt.datetime.now()
    filename='DublinBike'
    timestamp_format=dt.datetime.timestamp(datetime_now)
    fn='{}_{}'.format(filename,timestamp_format)
    fp='{}/{}.txt'.format(filepath,fn)    
    json_atrib_ordered=['number'
                          , 'contract_name'
                          , 'name'
                          , 'address'
                          , 'banking'
                          , 'bonus'
                          , 'bike_stands'
                          , 'available_bike_stands'
                          , 'available_bikes'
                          , 'status'
                          , 'position.lat'
                          , 'position.lng'
                          , 'last_update']
    
    json_atrib_rename_dict={
                            'position.lat':'position_latitude'
                          , 'position.lng':'position_longitude'
    }
    
    
    #Error handling
    error_dictionary={
                        0:'Success'
                        ,1:'The filepath does not exist. You entered:\n{}'
                        ,2:'There was an error reading dataframe.'
                        ,3:'Json Payload Doesnt Match Columns'
                        ,4:'Error Saving to File'
                        }
    
    #Assume no error by default
    error_code=0
    
    
    #Check that the filepath exists
    if os.path.exists(filepath) or (filepath=='' or filepath=='.'):
        
        #Read Dataframe
        try:
            df=pd.json_normalize(json)
            
            if filepath=='' or filepath=='.':
                fp='{}/{}.txt'.format(os.getcwd(),fn)
            
            #Columns Match
            if set(df.columns)==set(json_atrib_ordered):
                print('Columns match')
                
                #Try Write CSV
                try:
                    df=df[json_atrib_ordered]
                    df=df.rename(columns=json_atrib_rename_dict)                
                    df.to_csv(fp, sep='|', index=False)
                    print('Written')
                
                except:
                    error_code=4
                    error_message=error_dictionary[error_code].format(filepath)
                    print(error_message)
                    print('Error in Ordering and Saving')
            
            #Error In Columns
            else:
                error_code=3
                error_message=error_dictionary[error_code].format(filepath)
                print(error_message)
               
        #Error Reading Dataframe
        except:
            error_code=2
            error_message=error_dictionary[error_code].format(filepath)
            print(error_message)
        
    #File path does not exist
    else:
        error_code=1
        error_message=error_dictionary[error_code].format(filepath)
        print(error_message)
        
    return [error_code,fp]




####--------------------------------------
#05. Connect to a Database Engine
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
        
    except Exception as e:
        error_code=1
        error_message=error_dictionary[error_code]
        print(error_message)
        print("The Exception is:\n\n{}\n\n".format(e))
    
    return [error_code,engine]


####--------------------------------------
#06. Setup the Database Schema and all related functions (e.g. foreign keys, primary keys)
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
#07. Retrieve the unique station numbers from the station table
####--------------------------------------



def existing_station_numbers(engine):
    """A function to check which station numbers are already in the database"""
    station_list=[]
    
    try:
        Select_SQL="""
        SELECT
            number
        FROM
            01_station
        """

        result=engine.execute(Select_SQL)

        rows = result.fetchall()

        for station_number in rows:
            print(station_number)
            station_list+=[station_number[0]]
            
        result.close()
            
    except:
        print('Test')
        station_list=[]
        
        
    return station_list


####--------------------------------------
#08. Insert values to availability and station table
####--------------------------------------





####--------------------------------------
#08.1 WEATHER DATA
####--------------------------------------

def request_weather_data(latitude,longitude):
    """Request OpenWeather Data.
    
    Inpu: Key
    Output: JsonTEXT
    """
    print("Inside request_weather_data()\n\n")

    key=services_dictionary['OpenWeatherAPI']['API Key']
    endpoint=services_dictionary['OpenWeatherAPI']['Endpoint']['weather_at_coord']

    
    #Error handling
    error_dictionary={
                         0:'Success'
                        ,1:'There was an error in the request'
                        }
    
    #Assume no error by default
    error_code=0
    
    #Attempt the Request
    try:
        request_response=rq.get(endpoint,params={"APPID":key,
                                                        "lat":latitude,
                                                        "lon":longitude
                                                       })
        
        json_text=request_response.json()
        
    #Failed for some reason
    except Exception as e:
        error_code=1
        error_message=error_dictionary[error_code]
        json_text=''
        json_response=''
        
        print(error_message)
        print(e)
        

    return [error_code,json_text]


def store_weather_data(weather_json,number,avail_datetime_updated,engine,time_added):
    """Store the Weather Data into the database"""
    
    print('Inside store_weather_data')
    station_number=number
    avail_dt_update=avail_datetime_updated
    position_long=weather_json['coord']['lon']
    position_lat=weather_json['coord']['lat']
    
    weather_id=weather_json['weather'][0]['id']
    main=weather_json['weather'][0]['main']
    description=weather_json['weather'][0]['description']
    icon=weather_json['weather'][0]['icon']
    icon_url='http://openweathermap.org/img/wn/{}@2x.png'.format(icon)
    
    base=weather_json['base']
    temp=weather_json['main']['temp']
    feels_like=weather_json['main']['feels_like']
    temp_min=weather_json['main']['temp_min']
    temp_max=weather_json['main']['temp_max']
    pressure=weather_json['main']['pressure']
    humidity=weather_json['main']['humidity']
    visibility=weather_json['visibility']
    
    wind_speed=weather_json['wind']['speed']
    wind_degree=weather_json['wind']['deg']
    
    clouds_all=weather_json['clouds']['all']
    
    datetime=weather_json['dt']
    sys_type=weather_json['sys']['type']
    sys_country=weather_json['sys']['country']
    sys_id=weather_json['sys']['id']
    sys_sunrise=weather_json['sys']['sunrise']
    sys_sunset=weather_json['sys']['sunset']
    
    timezone=weather_json['timezone']
    id_var=weather_json['id']
    name=weather_json['name']
    cod=weather_json['cod']
    
    created_date=time_added
    
    weather_insert='''INSERT INTO 01_weather
    
                                (    number
                                    ,position_long
                                    ,position_lat

                                    ,weather_id
                                    ,main
                                    ,description
                                    ,icon
                                    ,icon_url

                                    ,base
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

                                    ,datetime
                                    ,sys_type
                                    ,sys_id
                                    ,sys_country

                                    ,sys_sunrise
                                    ,sys_sunset

                                    ,timezone
                                    ,id
                                    ,name
                                    ,cod
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
                    ,base
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
                    ,datetime
                    ,sys_type
                    ,sys_id
                    ,sys_country
                    ,sys_sunrise
                    ,sys_sunset
                    ,timezone
                    ,id_var
                    ,name
                    ,cod
                    ,created_date)
    
    engine.execute(weather_insert,weather_values)

    return

def insert_station_static_values(json_data,existing_station_numbers, engine):
    """Insert the static values into the database"""
    
    print(f"Inside insert_station_static_values()\n\n")
    
    station_list=existing_station_numbers
    datetime_now=dt.datetime.now()
    created_date=dt.datetime.timestamp(datetime_now)
          
    for entry in json_data:
        address=entry['address']
        name=entry['name']
        contract_name=entry['contract_name']
        banking=int(entry['banking'])
        bonus=int(entry['bonus'])
        bike_stands=entry['bike_stands']
        available_bike_stands=entry['available_bike_stands']
        available_bikes=entry['available_bikes']
        status=entry['status']
        number=entry['number']
        position_lat=entry['position']['lat']
        position_lng=entry['position']['lng']
        last_update=entry['last_update']/1000
        

        
        ###RENAME STATION
        station_insert='''INSERT INTO 01_station 
                                (address
                                  ,banking
                                  ,bike_stands
                                  ,bonus
                                  ,contract_name
                                  ,name
                                  ,number
                                  ,position_lat
                                  ,position_long
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
                                  ,%s)
                                    '''
        
        
        
        variable_insert='''INSERT INTO 01_availability 
                                (number
                                ,available_bikes
                                ,available_bike_stands
                                ,last_update
                                ,created_date)
                                  
                            VALUES
                                  (%s
                                  ,%s
                                  ,%s
                                  ,%s
                                  ,%s)
                                        '''
        
        #Station Data already available
        if number not in station_list:
            station_values=(address,banking,bike_stands ,bonus,contract_name,name,number,position_lat,position_lng,created_date)
            engine.execute(station_insert,station_values)
    
        bike_values=(number,available_bikes,available_bike_stands,last_update,created_date)
        engine.execute(variable_insert,bike_values)

        try:
            weather_info_json_lat_long_list=request_weather_data(latitude=str(position_lat),longitude=str(position_lng))
            weather_info_json_lat_long_json=weather_info_json_lat_long_list[1]
            store_weather_data(weather_info_json_lat_long_json,number,last_update,engine,created_date)
        except Exception as e:
            print(e)

            

    return




####--------------------------------------
#10. Pull Station Data, Post to DB
####--------------------------------------

#Wrapper function to pull the bike data and store it into a database
def pull_station_data():
    """Pull Weather Data and save it into the database."""
    
    print("Inside pull_station_data()\n\n")

    try:
        request_list=request_dublinbike_data()
        json_data=request_list[1]

        #No error occured
        if request_list[0]==0:
            myhost=database_dictionary['endpoint']
            myuser=database_dictionary['username']
            mypassword=database_dictionary['password']
            myport=database_dictionary['port']
            mydb=database_dictionary['database']

            mysql_list=connect_db_engine(myhost,myuser,mypassword,myport,mydb)
            mysql_engine=mysql_list[1]
            existing_station_numbers_list=existing_station_numbers(mysql_engine)
            insert_station_static_values(json_data,existing_station_numbers_list,mysql_engine)
            mysql_engine.dispose()
            
        else:
            print('There had been an error')

    except Exception as e:
        print(e)

    return



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

    while True:
        
        #Pull it every five miutes
        try:
            print("-------------------------------\n\n\n")
            print("-------------------------------\n\n\n")
            print("-------------------------------\n\n\n")
            print('''Starting: The time now is: {}'''.format(dt.datetime.now()))
            pull_station_data()
            time.sleep(5*60)
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