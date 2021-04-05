from FlaskApp.methods import *
from FlaskApp.data_dictionary import database_dictionary, fr_database_dictionary, js_database_dictionary
import requests

myhost=database_dictionary['endpoint']
myuser=database_dictionary['username']
mypassword=database_dictionary['password']
myport=database_dictionary['port']
mydb=database_dictionary['database']


engine = connect_db_engine(myhost,myuser,mypassword,myport,mydb)
engine = engine[1]

def main():
    """Function to loop through each station and call the weather forecast function for the coordinates of each station
    This could alternatively be done by pulling the station co-ordinates from our database instead of making an api call
    """
    # Set up the forecast table if it hasn't been done already
    setup_database(myhost, myuser, mypassword, myport, mydb)
    #Get the current date for when this function is called to be able to group all entries together
    datetime_now = dt.datetime.now()
    created_date = dt.datetime.timestamp(datetime_now)
    station_data = get_bike_station_data()

    # Loop through each bike station to get their coordinates and make a forecast call on those coordinates
    for station in station_data:
        position_lat = station['position']['lat']
        position_lng = station['position']['lng']
        number = station['number']
        print("**************")
        print(f"Current station is station number {number} ")
        print("**************")
        # Get the forecast for the co-ordinates of the current station in the loop
        weather_json = getWeatherForecast(position_lat, position_lng)
        # Store the forecast for this station in the database
        store_weather_forecast(weather_json, number, engine, created_date)
    print("**************")
    print("Forecasts inserted for all stations!")
    print("**************")
    return


def get_bike_station_data():
    """Function to return data for each station"""
    NAME = "Dublin"
    STATIONS = "https://api.jcdecaux.com/vls/v1/stations"
    APIKEY = "89479cb592a43f7745c15eb783af62fa5c12bd3c"
    r = requests.get(STATIONS, params={"apiKey": APIKEY, "contract": NAME})
    station_data = json.loads(r.text)
    return station_data

def getWeatherForecast(latitude, longitude):
    """Function to return the weather forecast for certain co-ordinates"""
    weather_key = "71aa44a6a3a027964138e4aa742c650f"
    weather_by_coordinates = 'http://api.openweathermap.org/data/2.5/forecast'
    r = requests.get(weather_by_coordinates, params={"APPID": weather_key, "lat": latitude, "lon": longitude})
    return r.json()

def existing_station_numbers(engine):
    """A function to check which station numbers are already in the database"""
    df = pd.read_sql_table("01_station", engine)
    station_list = df['number'].tolist()
    return station_list



def store_weather_forecast(weather_json,number,engine,time_added):
    """
    Store the Weather Data into the database
    Removed base, timezone, avail_update_dt, datetime, id_var, name, cod and all 'sys' entries when compared to scraper for current weather
    Added forecast_time_dt and forecast_time_txt
    """

    print('Inside store_weather_forecast')
    station_number=number
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

    return

if __name__ == '__main__':
    main()