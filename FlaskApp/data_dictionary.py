##------------------APP---------------##
## 
##User:     Disappster
##DC:       2021-03-01
##DLM:      2021-03-01
##MC:       COMP30830
##SD:       Database and schema dictionaries for easy access
##
##------------------APP---------------##


ar_database_dictionary={
                        'username':'adamryan'
                        ,'password':'adam.ryan1'
                        ,'database':'dbbikes'
                        ,'endpoint':'dbbikes.cmbuuvrlonfv.us-east-1.rds.amazonaws.com'
                        ,'port':'3306'    
                    }


database_dictionary={
                        'username':'admin'
                        ,'password':'DublinBikesProject2201'
                        ,'database':'dublin_bikes'
                        ,'endpoint':'dublin-bikes.ciu0f2oznjig.us-east-1.rds.amazonaws.com'
                        ,'port':'3306'    
                    }

js_database_dictionary={
                        'username':'janeslevin'
                        ,'password':'js2021dbbikes'
                        ,'database':'dbbikes30830'
                        ,'endpoint':'dbbikes30830.cfv8ckdtpwoq.us-east-1.rds.amazonaws.com'
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