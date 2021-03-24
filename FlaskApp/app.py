##------------------APP---------------##
## 
##User:     Disappster
##DC:       2021-03-01
##DLM:      2021-03-01
##MC:       COMP30830
##SD:       FLASK APP
##
##------------------APP---------------##


######---------BEGIN
#     FLASK
######--------END

from flask import Flask, render_template
from FlaskApp.methods import *
from FlaskApp.data_dictionary import database_dictionary, fr_database_dictionary,js_database_dictioanry

app = Flask(__name__)

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

######---------BEGIN
#     BEGIN VIEWS
######--------END

@app.route("/debug")
def debug_hellow():
    return "Hello World"

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/")
@app.route("/home")
@app.route("/index")
def home():
    station_Data = get_stations_json(host=myhost,user=myuser,password=mypassword,port=myport,db=mydb)
    print(station_Data)
    stationData=json.loads(station_Data)
    return render_template('index.html', station_data=stationData)

@app.route("/stations")
def station():
    station = get_stations_json(host=myhost,user=myuser,password=mypassword,port=myport,db=mydb)
    return station


@app.route("/availability")
def availability_request():
    result=availability_limit_df(host=myhost,user=myuser,password=mypassword,port=myport,db=mydb)
    return result

@app.route("/availability_v2")
def recentUpdate():
    avail_df=availability_recentUpdate(host=myhost,user=myuser,password=mypassword,port=myport,db=mydb)
    return avail_df.to_json(orient='records')


if __name__=="__main__":
    print('Running')
    app.run(debug=True,port=5000)