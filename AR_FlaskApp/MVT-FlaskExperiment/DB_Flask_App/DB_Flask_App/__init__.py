from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from DB_Flask_App.config import *

app = Flask(__name__)
app.config['SECRET_KEY'] = secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from DB_Flask_App import models, views
