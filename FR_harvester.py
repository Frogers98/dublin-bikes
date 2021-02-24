#!/usr/bin/env python
# coding: utf-8
import traceback
from datetime import datetime
import requests
import json
import pandas as pd
from sqlalchemy import create_engine
import time


def store():
    # Connect to the api and store the response in a variable
    NAME = "Dublin"
    STATIONS = "https://api.jcdecaux.com/vls/v1/stations"
    APIKEY = "89479cb592a43f7745c15eb783af62fa5c12bd3c"
    r = requests.get(STATIONS, params={"apiKey": APIKEY, "contract": NAME})
    data = json.loads(r.text)

    # Make dataframe and rename the co-ordinates so sql queries can execute correctly
    df = pd.json_normalize(data)
    df.rename(columns={'position.lat': 'position_lat', 'position.lng': 'position_lng'}, inplace=True)

    # Convert last_update to date time to keep track of when things are pulled from api
    df['last_update'] = pd.to_datetime(df['last_update'], unit='ms')

    # Split the dataframe into station and availability
    df_station = df[['address', 'banking', 'bike_stands', 'bonus', 'contract_name', 'name', 'number', 'position_lat',
                     'position_lng']]
    df_availability = df[['number', 'available_bikes', 'available_bike_stands', 'last_update']]
    df_availability['pull_time'] = pd.to_datetime('now')

    # Set database settings
    URI = "dublin-bikes.ciu0f2oznjig.us-east-1.rds.amazonaws.com"
    PORT = "3306"
    DB = "dublin_bikes"
    USER = "admin"
    PASSWORD = "DublinBikesProject2201"

    # Store the database schema in a dictionary
    db_schema = {
        '01_station': {
            'number': 'INTEGER',
            'name': 'VARCHAR(256)',
            'address': 'VARCHAR(256)',
            'banking': 'INTEGER',
            'bike_stands': 'INTEGER',
            'bonus': 'INTEGER',
            'contract_name': 'VARCHAR(256)',
            'position_lat': 'REAL',
            'position_lng': 'REAL',
        }
        , '01_availability': {
            'entry_id': 'INTEGER',
            'number': 'INTEGER',
            'available_bikes': 'INTEGER',
            'available_bike_stands': 'INTEGER',
            'last_update': 'DATETIME',
            'pull_time': 'DATETIME',
        }
    }

    # Set up database connection
    engine = create_engine('mysql+mysqlconnector://{}:{}@{}:{}/{}'.format(USER, PASSWORD, URI, PORT, DB, echo=True))
    connection = engine.connect()

    def setup_tables(db_schema):
        """Set up the tables in the database if they do not already exist
         commented out for now as I've already set up the tables, can change this at any stage"""

    for table, columns in db_schema.items():
        column_count = 0
        num_columns = len(columns)
        sql = """CREATE TABLE IF NOT EXISTS {} (\n""".format(table)
        insert_row = ''

        for column_heading, data_type in columns.items():
            if column_count > 0:
                insert_row += ", {} {}".format(column_heading, data_type)
            else:
                insert_row += "{} {} NOT NULL AUTO_INCREMENT PRIMARY KEY".format(column_heading, data_type)
                column_count += 1

        sql += "{})".format(insert_row)
        engine.execute(sql)
    setup_tables(db_schema)

    # Store the pulled data in the database
    # The station table is commented out for now because I don't think it needs to be updated continuously and i've already updated it once
    # df_station.to_sql(name='01_station', con=connection, if_exists='append', index=False)
    df_availability.to_sql(name='01_availability', con=connection, if_exists='append', index=False)

    # Close connection to database
    connection.close()


def main():
    # Run forever
    while True:
        try:
            store()
            # Sleep for 5 mins
            time.sleep(5 * 60)
        except:
            # Print traceback and break if there's an error
            print(traceback.format_exc())
            break


if __name__ == "__main__":
    main()
