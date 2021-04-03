##------------------APP---------------##
## 
##User:     Disappster
##DC:       2021-03-01
##DLM:      2021-03-01
##MC:       COMP30830
##SD:       Database and schema dictionaries for easy access
##
##------------------APP---------------##


database_dictionary={
                        'username':'adamryan'
                        ,'password':'adam.ryan1'
                        ,'database':'dbbikes'
                        ,'endpoint':'dbbikes.cmbuuvrlonfv.us-east-1.rds.amazonaws.com'
                        ,'port':'3306'    
                    }


fr_database_dictionary={
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

                    ,'02_availability_train':{
                                'number':'INTEGER'
                                ,'available_bikes':'INTEGER'
                                ,'available_bike_stands':'INTEGER'
                                ,'last_update':'BIGINT'
                                ,'created_date':'BIGINT'
                                }
,                   '02_availability_test':{
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