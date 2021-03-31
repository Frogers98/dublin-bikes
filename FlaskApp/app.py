##------------------APP---------------##
## 
##User:     Disappster
##DC:       2021-03-01
##DLM:      2021-03-01
##MC:       COMP30830
##SD:       FLASK APP VIEWS AND RUN COMBINED
##
##------------------APP---------------##

####--------------------------------------
#00.Import Modules
####--------------------------------------

######---------BEGIN
#     FLASK
######--------END

from flask import Flask, render_template
from FlaskApp.methods import *
from FlaskApp.data_dictionary import database_dictionary, fr_database_dictionary, js_database_dictionary



####--------------------------------------
#01. DEFINE APP
####--------------------------------------

app = Flask(__name__)


####--------------------------------------
#02.DEFINE DATABASE CONNECTION
####--------------------------------------

myhost=database_dictionary['endpoint']
myuser=database_dictionary['username']
mypassword=database_dictionary['password']
myport=database_dictionary['port']
mydb=database_dictionary['database']

# myhost=fr_database_dictionary['endpoint']
# myuser=fr_database_dictionary['username']
# mypassword=fr_database_dictionary['password']
# myport=fr_database_dictionary['port']
# mydb=fr_database_dictionary['database']

# myhost=js_database_dictionary['endpoint']
# myuser=js_database_dictionary['username']
# mypassword=js_database_dictionary['password']
# myport=js_database_dictionary['port']
# mydb=js_database_dictionary['database']


####--------------------------------------
#03.DEFINE VIEWS
####--------------------------------------

@app.route("/debug")
def debug_hello():
    """A debug page to check if the flask app is running"""
    return "Hello World"

@app.route("/about")
def about():
    """An about page to show about stuff - maybe we can make this the main page?"""

    # graph_df=stations_by_day(host=myhost,user=myuser,password=mypassword,port=myport,db=mydb)
    # print(graph_df)
    
    return render_template('about.html')

@app.route("/")
@app.route("/home")
@app.route("/index")
def home():
    """Returns the Home Route"""
    station_data = station_availability_last_update_table_df(host=myhost,user=myuser,password=mypassword,port=myport,db=mydb)
    
    #Turn the dataframe into the json
    station_data_json=station_data.to_json(orient="records")
    
    #Load the json into the front end
    stationData=json.loads(station_data_json)
    # This sorts the list station dictionaries by name so the selector will be ordered alphabetically
    stationDataSorted = sorted(stationData, key=lambda i: i['name'])
    return render_template('index.html', station_data=stationDataSorted)

@app.route("/stations")
def station():
    """Returns the station Json Data"""

    #Return the station info
    station = station_availability_last_update_table_df(host=myhost,user=myuser,password=mypassword,port=myport,db=mydb)
    
    #Turns that into a json
    station_data_json=station.to_json(orient="records")

    return station_data_json


@app.route("/availability")
def availability_request():
    """Returns a dataframe of the station and availability data"""

    result=station_availability_last_update_table_df(host=myhost,user=myuser,password=mypassword,port=myport,db=mydb)
    
    return result


###----ROUTES FOR ANALYTICS----####

###----All Station Averages----####


@app.route("/station_availability_stat_by_weekdayno")
def station_availability_stat_by_weekdayno():
    """Returns a dataframe of the station and availability data"""
    result=avg_station_availability_by_weekdayno_df(host=myhost,user=myuser,password=mypassword,port=myport,db=mydb)
    
    result=result.to_json(orient="records")

    return result

@app.route("/station_availability_stat_by_date")
def station_availability_stat_by_date():
    """Returns a dataframe of the station and availability data"""

    result=avg_station_availability_by_date_df(host=myhost,user=myuser,password=mypassword,port=myport,db=mydb)
    result=result.to_json(orient="records")

    return result


@app.route("/station_availability_stat_by_monthno")
def station_availability_stat_by_monthno():
    """Returns a dataframe of the station and availability data"""

    result=avg_station_availability_by_monthno_df(host=myhost,user=myuser,password=mypassword,port=myport,db=mydb)
    result=result.to_json(orient="records")

    return result

@app.route("/station_availability_stat_by_hourno")
def station_availability_stat_by_hourno():
    """Returns a dataframe of the station and availability data"""

    result=avg_station_availability_by_hourno_df(host=myhost,user=myuser,password=mypassword,port=myport,db=mydb)
    result=result.to_json(orient="records")

    return result


@app.route("/station_availability_stat_by_weekno")
def station_availability_stat_by_weekno():
    """Returns a dataframe of the station and availability data"""

    result=avg_station_availability_by_weekno_df(host=myhost,user=myuser,password=mypassword,port=myport,db=mydb)
    result=result.to_json(orient="records")

    return result


###----Specific Station Averages----####
@app.route("/single_station_availability_stat_by_weekdayno/<no>")
def single_station_availability_stat_by_weekdayno(no):
    """Returns a dataframe of the station and availability data"""
    result=avg_station_availability_by_weekdayno_df_forstat(host=myhost,user=myuser,password=mypassword,port=myport,db=mydb,station_no=no)
    
    result=result.to_json(orient="records")

    return result


@app.route("/single_station_availability_stat_by_date/<no>")
def single_station_availability_stat_by_date(no):
    """Returns a dataframe of the station and availability data"""

    result=avg_station_availability_by_date_df_forstat(host=myhost,user=myuser,password=mypassword,port=myport,db=mydb,station_no=no)
    result=result.to_json(orient="records")

    return result


@app.route("/single_station_availability_stat_by_monthno/<no>")
def single_station_availability_stat_by_monthno(no):
    """Returns a dataframe of the station and availability data"""

    result=avg_station_availability_by_monthno_df_forstat(host=myhost,user=myuser,password=mypassword,port=myport,db=mydb,station_no=no)
    result=result.to_json(orient="records")

    return result

@app.route("/single_station_availability_stat_by_hourno/<no>")
def single_station_availability_stat_by_hourno(no):
    """Returns a dataframe of the station and availability data"""

    result=avg_station_availability_by_hourno_df_forstat(host=myhost,user=myuser,password=mypassword,port=myport,db=mydb,station_no=no)
    result=result.to_json(orient="records")

    return result


@app.route("/single_station_availability_stat_by_weekno/<no>")
def single_station_availability_stat_by_weekno(no):
    """Returns a dataframe of the station and availability data"""

    result=avg_station_availability_by_weekno_df_forstat(host=myhost,user=myuser,password=mypassword,port=myport,db=mydb,station_no=no)
    result=result.to_json(orient="records")

    return result


###----Specific Station Average Wrapper----####
@app.route("/metric/<metric_type>/<station_no>")
def metric_type_average_avail_for_station(metric_type,station_no):
    """Returns a dataframe of the station and availability data"""

   #Hour 
    if metric_type=='Hours':
        result_json=single_station_availability_stat_by_hourno(no=station_no)

    #Weekday
    elif metric_type=='Day':
        result_json=single_station_availability_stat_by_weekdayno(no=station_no)

    #Month
    elif metric_type=='Month':
        result_json=single_station_availability_stat_by_monthno(no=station_no)

    #Date
    elif metric_type=='Date':
        result_json=single_station_availability_stat_by_date(no=station_no)

    #Week
    elif metric_type=='Week':
        result_json=single_station_availability_stat_by_weekno(no=station_no)

    else:
        print('Unknown Metric and Week')

    return result_json


@app.route("/availability_v2")
def recentUpdate():
    """Recent Update"""
    avail_df=availability_recentUpdate(host=myhost,user=myuser,password=mypassword,port=myport,db=mydb)
    return avail_df.to_json(orient='records')



###----RUN----####

from FlaskApp.tests import run_tests

if __name__=="__main__":
    print('Running')

    test_result=False
    test_result=run_tests(host=myhost,user=myuser,password=mypassword,port=myport,db=mydb)

    #Check if the python test cases run alright
    if test_result:
        app.run(debug=True,port=5000)