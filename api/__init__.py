from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import json
import os

# Path to database configuration file in the tasks folder
configPath = os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'tasks')) + '/config.json'
dbConfig = json.load(open(configPath))['database']

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{dbConfig['user']}:{dbConfig['password']}@{dbConfig['host']}:{dbConfig['port']}/{dbConfig['dbname']}"
db = SQLAlchemy(app)

from api import routes