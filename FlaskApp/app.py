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
from FlaskApp.data_dictionary import database_dictionary

app = Flask(__name__)

myhost=database_dictionary['endpoint']
myuser=database_dictionary['username']
mypassword=database_dictionary['password']
myport=database_dictionary['port']
mydb=database_dictionary['database']

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
    return render_template('index.html')

@app.route("/station")
def station():
    station_df=station_availability_last_update_table_df(host=myhost,user=myuser,password=mypassword,port=myport,db=mydb)
    station_json=station_df.to_json(orient='records')
    return station_json

if __name__=="__main__":
    print('Running')
    app.run(debug=True,port=5000)