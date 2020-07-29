from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import Column, Integer, DateTime
from flask_cors import CORS
import json 
import os
import datetime
import requests
from garden_utils import *

# app = Flask(__name__)
# cors = CORS(app)

# basedir = os.path.abspath(os.path.dirname(__file__))
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'garden.sqlite')
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'False'

# db = SQLAlchemy(app)
# ma = Marshmallow(app)

_NOT_POSTED = 0
_POSTED = 1
_CANCELED = 2

################################################## M O D E L S ##################################################
class Medicao(db.Model):
    __tablename__ = 'medicoes'
    idMedicao = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.Integer, unique=False)
    tipo = db.Column(db.String(80), unique=False)
    medida = db.Column(db.Integer, unique=False)
    status = db.Column(db.Integer, unique=False)
    idSensor = db.Column(db.Integer, db.ForeignKey("sensores.idSensor", ondelete=None))
    

    def __init__(self, timestamp, tipo, medida, idSensor, status=_NOT_POSTED):
        self.timestamp = timestamp
        self.tipo = tipo
        self.medida = medida
        self.idSensor = idSensor
        self.status = status

################################################## S C H E M A ##################################################
class MedicaoSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('idMedicao', 'timestamp', 'tipo', 'medida', 'status', 'idSensor')

medicao_schema = MedicaoSchema()
medicoes_schema = MedicaoSchema(many=True)

################################################## R O U T E S ##################################################
@app.route("/")
def medicao_homepage():
    text = "Este eh o backend do sistema de IoG - Internet of Gardens. Voce pode acessar os endpoints aqui descritos."

    response = {
        "status_code": 200,
        "message": text,
        "/medicao [POST]": "adiciona um medicao ao jardim",
        "/medicao [GET]": "retorna as informações de todos os medicaoes",
        "/medicao/<id> [GET]": "retorna as informações do medicao com o id especificado",
        "/medicao/<id> [PUT]": "atualiza as informações do medicao com o id especificado",
        "/medicao/<id> [DELETE]": "deleta o medicao com o id especificado",
    } 
    return jsonify(response)


# endpoint to create new line
@app.route("/medicao", methods=['POST'])
def add_medicao():
    if request.method == 'POST':
        timestamp = request.json['timestamp']
        tipo = request.json['tipo']
        medida = request.json['medida']
        idSensor = request.json['idSensor']

        new_medicao = Medicao(timestamp, tipo, medida, idSensor)
        db.session.add(new_medicao)
        db.session.commit()

        response = medicao_schema.dump(new_medicao)
        print("\n \n \n \n")
        print(response,type(response))
        print("\n \n \n \n")
        
        return jsonify(response)

# endpoint to show all lines
@app.route("/medicao", methods=['GET'])
def get_medicao():
    if request.method == 'GET':
        all_medicoes = Medicao.query.all()
        
        response = medicoes_schema.dump(all_medicoes)
        
        return jsonify(response)
        
# @app.route("/medicao/unposted", methods=['GET'])
def get_unposted_medicoes():
    # if request.method == 'GET':
    medicoes = Medicao.query.filter(Medicao.status==_NOT_POSTED)
    
    response = medicoes_schema.dump(medicoes)
    
    return response


# endpoint to get line detail by id
@app.route("/medicao/<id>", methods=["GET"])
def medicao_detail(id):
    if request.method == 'GET':
        medicao = Medicao.query.get(id)
        response = medicao_schema.dump(medicao)

        return jsonify(response)

# # endpoint to update line
# @app.route("/medicao/<id>", methods=["PUT"])
# def medicao_update(id):
#     if request.method == 'PUT':

#         sensor = Sensor.query.get(id)

#         if sensor is not None:
#             if 'codigo' in request.json.keys():
#                 sensor.codigo = request.json['codigo']
#             if 'tipo' in request.json.keys():
#                 sensor.tipo = request.json['tipo']
#             if 'idUsuario' in request.json.keys():
#                 sensor.idUsuario = request.json['idUsuario']
            
#             db.session.commit()

#             return sensor_schema.jsonify(sensor)

#         return None

# endpoint to delete line
@app.route("/medicao/<id>", methods=["DELETE"])
def medicao_delete(id):
    if request.method == 'DELETE':
        medicao = Medicao.query.get(id)
        if medicao is not None:
            db.session.delete(medicao)
            db.session.commit()

            return medicao_schema.jsonify(medicao)
        return None


############################################################################################################

if __name__ == '__main__':
    app.run(debug=True)