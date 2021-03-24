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
from FlaskApp.data_dictionary import database_dictionary, fr_database_dictionary,js_database_dictioanry



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

#myhost=fr_database_dictionary['endpoint']
#myuser=fr_database_dictionary['username']
#mypassword=fr_database_dictionary['password']
#myport=fr_database_dictionary['port']
#mydb=fr_database_dictionary['database']

#myhost=js_database_dictionary['endpoint']
#myuser=js_database_dictionary['username']
#mypassword=js_database_dictionary['password']
#myport=js_database_dictionary['port']
#mydb=js_database_dictionary['database']


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

    return render_template('index.html', station_data=stationData)

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

@app.route("/availability_v2")
def recentUpdate():
    """Recent Update"""
    avail_df=availability_recentUpdate(host=myhost,user=myuser,password=mypassword,port=myport,db=mydb)
    return avail_df.to_json(orient='records')


from FlaskApp.tests import run_tests

if __name__=="__main__":
    print('Running')

    test_result=False
    test_result=run_tests(host=myhost,user=myuser,password=mypassword,port=myport,db=mydb)

    #Check if the python test cases run alright
    if test_result:
        app.run(debug=True,port=5000)