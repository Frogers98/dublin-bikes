from DB_Flask_App import db
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.mysql import DOUBLE
from sqlalchemy import inspect, create_engine
from DB_Flask_App.config import *
import datetime as dt
import pandas as pd




#Class for Station Data
class Station(db.Model):
    """Station Table. Holds Static Station Data"""

    __tablename__ = 'station'

    #Station Number
    number=db.Column(db.Integer,primary_key=True)

    #Address Name
    address=db.Column(db.String(256),unique=False,nullable=False)

    #Banks
    banking=db.Column(db.Integer,unique=False,nullable=False)

    #Total Bike stands
    bike_stands=db.Column(db.Integer,unique=False,nullable=False)

    #Bonus
    bonus=db.Column(db.Integer,unique=False,nullable=False)

    #Name of Station
    contract_name=db.Column(db.String(256),unique=False,nullable=False)

    #Name of Station
    name=db.Column(db.String(256),unique=False,nullable=False)

    #Latitude of Bike Station
    position_lat=db.Column(db.Float(),unique=False,nullable=False)

    #Longitude of Bike Station
    position_long=db.Column(db.Float(),unique=False,nullable=False)

    #When was the entry into the Database
    created_date=db.Column(db.BIGINT,unique=False,nullable=False,default=dt.datetime.timestamp(dt.datetime.now()))

    ###Relationships

    #Availability
    station_availability=db.relationship('Availability',backref='station_number',lazy=True)

    #Weather
    station_weather=db.relationship('Weather',backref='station_number',lazy=True)

    def __repr__(self):
        """Return View of Self"""
        station_number = self.number
        station_name = self.name
        station_pos = """Lat: {} Long: {}""".format(self.position_lat,self.position_long)
        station_created = dt.datetime.fromtimestamp(self.created_date)
        station_bike_stands=self.bike_stands

        print_statement="""Station Number: {}\n
                            Station Name: {}\n
                            Position: {}\n
                            Bike Stands: {}\n
                            Posted On: {}\n\n
                            """.format(station_number
                                        ,station_name
                                        ,station_pos
                                        ,station_bike_stands
                                        ,station_created).replace("                            ","",-1)

        return print_statement

    @classmethod
    def to_dict(self):
        """Convert Model to Dictionary
        
        Source: https://stackoverflow.com/questions/5022066/how-to-serialize-sqlalchemy-result-to-json
        """

        column_attribs=inspect(self).mapper.column_attrs 
        return_dict={}

        for col in column_attribs:
            col_name=col.key
            col_val=getattr(self, col_name)
            print("{}:{}".format(col_name,col_val))
            return_dict[col_name]=col_val

        return return_dict

    @classmethod
    def to_df(self):
        """Convert a model to dataframe.

        Return dataframe
        """
        connect=db.engine.connect()
        df=pd.read_sql("Select * from {}".format(self.__tablename__),connect)
        connect.close()
        return df


#Class for Availability Data
class Availability(db.Model):
    """Availability Data"""

    __tablename__ = 'availability'
    
    #Primary Key
    id=db.Column(db.BIGINT,primary_key=True)
    
    #Station Number
    number=db.Column(db.Integer,db.ForeignKey('station.number'),nullable=False)
    
    #How many bikes are available?
    available_bikes=db.Column(db.Integer,unique=False,nullable=False)
    
    #How many bike stands are available?
    available_bike_stands=db.Column(db.Integer,unique=False,nullable=False)
    
    #What is the listed last updated date
    last_update=db.Column(db.BIGINT,unique=False,nullable=False)
    
    #When was the entry into the Database
    created_date=db.Column(db.BIGINT,unique=False,nullable=False,default=dt.datetime.timestamp(dt.datetime.now()))

    ###Relationships

    #Weather
    weather_at_time=db.relationship('Weather',backref='avail_id',lazy=True)



    def __repr__(self):
        """Return View of Self"""
        avail_number = self.number
        avail_id=self.id
        avail_available_bikes = self.available_bikes
        avail_bike_stands=self.available_bike_stands
        avail_percent=0

        if avail_bike_stands>0:
            avail_percent= 100*(avail_available_bikes/avail_bike_stands)
        
        avail_created = dt.datetime.fromtimestamp(self.created_date)
        avail_updated = dt.datetime.fromtimestamp(self.last_update)

        print_statement="""Station Number: {}\n
                            Availability ID: {}\n
                            Total Bike Stands: {}\n
                            Available Bike Stands: {} ({:.2f}%)\n
                            Updated On: {}
                            Posted On: {}\n\n
                            """.format(avail_number
                                        ,avail_id
                                        ,avail_bike_stands
                                        ,avail_available_bikes
                                        ,avail_percent
                                        ,avail_updated
                                        ,avail_created).replace("                            ","",-1)

        return print_statement

    @classmethod
    def to_dict(self):
        """Convert Model to Dictionary
        
        Source: https://stackoverflow.com/questions/5022066/how-to-serialize-sqlalchemy-result-to-json
        """

        column_attribs=inspect(self).mapper.column_attrs 
        return_dict={col.key: str(getattr(self, col.name)) for col in column_attribs}

        return return_dict


    @classmethod
    def to_df(self):
        """Convert a model to dataframe.

        Return dataframe
        """
        connect=db.engine.connect()
        df=pd.read_sql("Select * from {}".format(self.__tablename__),connect)
        connect.close()
        return df

#Class for Weather Data
class Weather(db.Model):
    """Weather Data"""

    __tablename__ = 'weather'

    #Primary Key of Weather Data
    id=db.Column(db.BIGINT,primary_key=True)
    
    #Position Longitude of Weather Reading
    position_long=db.Column(db.Float(),unique=False,nullable=False)
    
    #Position Latitude of Weather Reading
    position_lat=db.Column(db.Float(),unique=False,nullable=False)
    
    #Weather ID per API
    weather_id=db.Column(db.Integer,unique=False,nullable=False)
    
    #Main Weather Type
    main=db.Column(db.String(256),unique=False,nullable=False)
    
    #Weather Description
    description=db.Column(db.String(500),unique=False,nullable=False)
    
    #Weather Icon
    icon=db.Column(db.String(20),unique=False,nullable=False)
    
    #Weather Icon URL
    icon_url=db.Column(db.String(500),unique=False,nullable=False)
    
    #No Idea
    base=db.Column(db.String(256),unique=False,nullable=False)
    
    #Temperature
    temp=db.Column(db.Float(),unique=False,nullable=False)
    
    #What does the temperature Feel like
    feels_like=db.Column(db.Float(),unique=False,nullable=False)
    
    #What is the minimum temperature
    temp_min=db.Column(db.Float(),unique=False,nullable=False)
    
    #What is the maximum temperature
    temp_max=db.Column(db.Float(),unique=False,nullable=False)
    
    #Air Pressure
    pressure=db.Column(db.Integer,unique=False,nullable=False)
    
    #Humidity
    humidity=db.Column(db.Integer,unique=False,nullable=False)
    
    #Visibility Index
    visibility=db.Column(db.Integer,unique=False,nullable=False)
    
    #Wind Speed
    wind_speed=db.Column(db.Float(),unique=False,nullable=False)
    
    #Wind direction
    wind_degree=db.Column(db.Integer,unique=False,nullable=False)
    
    #Cloudy
    clouds_all=db.Column(db.Integer,unique=False,nullable=False)
    
    #Datetime of Update?
    datetime=db.Column(db.BIGINT,unique=False,nullable=False)
    
    #OpenWeatherMapAPI Type
    sys_type=db.Column(db.Integer,unique=False,nullable=False)

    #OpenWeatherMapAPI Station ID? 
    sys_id=db.Column(db.Integer,unique=False,nullable=False)

    #OpenWeatherMapAPI Country of Station
    sys_country=db.Column(db.String(10),unique=False,nullable=False)
    
    #OpenWeatherMapAPI Sunrise Time
    sys_sunrise=db.Column(db.BIGINT,unique=False,nullable=False)
    
    #OpenWeatherMapAPI Sunset Time
    sys_sunset=db.Column(db.BIGINT,unique=False,nullable=False)
    
    #OpenWeatherMapAPI Station Type?
    sys_type=db.Column(db.Integer,unique=False,nullable=False)
    
    #OpenWeatherMapAPI Timezone of the Station?
    timezone=db.Column(db.Integer,unique=False,nullable=False)
    
    #OpenWeatherMapAPI ???
    w_id=db.Column(db.BIGINT,unique=False,nullable=False)
    
    #OpenWeatherMapAPI Location Name
    name=db.Column(db.String(256),unique=False,nullable=False)
    
    #OpenWeatherMapAPI ???
    cod=db.Column(db.Integer,unique=False,nullable=False)
    
    #Date the field was added
    created_date=db.Column(db.BIGINT,unique=False,nullable=False,default=dt.datetime.timestamp(dt.datetime.now()))

    ###RelationShip Columns

    #Availability
    availability_id=db.Column(db.BIGINT,db.ForeignKey('availability.id'),nullable=False)
    
    #Station Number
    number=db.Column(db.Integer,db.ForeignKey('station.number'), nullable=False)


    def __repr__(self):
        """Return View of Self"""
        weather_station_number = self.number
        weather_type=self.description
        weather_availability_id=self.availability_id
        weather_update_date=dt.datetime.fromtimestamp(self.datetime)
        weather_posted_date=dt.datetime.fromtimestamp(self.created_date)
        weather_temperature=self.temp - 273.15 #Convert from Kelvin

        print_statement="""Station Number: {}\n
                            Availability ID: {}
                            Weather Type: {}\n
                            Temperature: {}°C\n
                            Updated On: {}
                            Posted On: {}\n\n
                            """.format(weather_station_number
                            ,weather_availability_id
                            ,weather_type
                            ,weather_temperature
                            ,weather_update_date
                            ,weather_posted_date).replace("                            ","",-1)

        return print_statement

    @classmethod
    def to_dict(self):
        """Convert Model to Dictionary
        
        Source: https://stackoverflow.com/questions/5022066/how-to-serialize-sqlalchemy-result-to-json
        """

        column_attribs=inspect(self).mapper.column_attrs 
        return_dict={col.key: str(getattr(self, col.name)) for col in column_attribs}

        return return_dict


    @classmethod
    def to_df(self):
        """Convert a model to dataframe.

        Return dataframe
        """
        connect=db.engine.connect()
        df=pd.read_sql("Select * from {}".format(self.__tablename__),connect)
        connect.close()
        return df