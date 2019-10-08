
# APP
from flask import Flask
app = Flask(__name__)

# CORS
from flask_cors import CORS
CORS(app)

# SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://administrador:@localhost:5432/biosql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy(app)

# Resources routes
from flask_restful import Api
routes = Api(app)
from .api import *
routes.add_resource(BiodbAPI, '/biodatabase', '/biodatabase/<id>')
routes.add_resource(FilesIO, '/upload/<biodb>', '/download')
routes.add_resource(Search, '/search')  # ?type=''&search=''
