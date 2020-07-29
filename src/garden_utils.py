from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import Column, Integer, DateTime
from flask_cors import CORS
import json 
import os
import datetime
import requests
# import atexit

_CLOUD_DOMAIN = "https://on00qnj8jh.execute-api.us-east-1.amazonaws.com/dev"

app = Flask(__name__)
cors = CORS(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'garden.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'False'

db = SQLAlchemy(app)
ma = Marshmallow(app)

def post_to_aws(path, object):
    print (object)
    url = _CLOUD_DOMAIN + "/" + path
    response = requests.post(url, json=object)
    return response


