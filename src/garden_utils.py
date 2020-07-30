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

_CLOUD_DOMAIN = "http://localhost:5000"

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

# ################################################################### #
# This function attempts to insert an object into the local database.
# If that succeeds, it attempts to insert that object into AWS DynamoDB.
# Multiple actions are necessary to guarantee the data persistance in 
# both DBs. When one of those fails, none of them occur.
# ################################################################### #
def synchronous_db_insert(object, object_schema, path):
    try:
        db.session.add(object)
        db.session.flush()
        sql_response = object_schema.dump(object)
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        print(" SQL ERROR! ". center(80, "#"))
        return jsonify({'SQL Error': str(e)}), 400

    try:
        aws_response = post_to_aws(path, sql_response)
    except Exception as e:
        db.session.rollback()
        db.session.flush()
        return jsonify({'AWS Error': str(e)}), 400

        db.session.commit()
    return jsonify(sql_response), 200
    
    



