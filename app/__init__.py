from flask import Flask
from flask_restful import Api
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
routes = Api(app)

from .api import *

routes.add_resource(BiodbAPI, '/biodatabase', '/biodatabase/<id>')
routes.add_resource(FilesIO, '/upload/<biodb>', '/download')
routes.add_resource(Search, '/search/<type>')

# @app.route('/path', methods=['POST'])

# @user.route('/<user_id>', defaults={'username': None})
# @user.route('/<user_id>/<username>')
# def show(user_id, username):
#     pass

# GET /customers/: get all customers
# GET /customers/[id]: get a customer by id
# POST /customers/: save a customer
# PUT /customers/update/[id]: update a customer by id
# DELETE /customers/[id]: delete a customer by id
