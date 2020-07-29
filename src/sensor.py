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

################################################## M O D E L S ##################################################
class Sensor(db.Model):
    __tablename__ = 'sensores'
    idSensor = db.Column(db.Integer, primary_key=True)
    codigo = db.Column(db.String(80), unique=False)
    tipo = db.Column(db.String(80), unique=False)
    # idUsuario = db.Column(db.Integer, db.ForeignKey("usuarios.idUsuario", ondelete='CASCADE'))
    idPlantacao = db.Column(db.Integer, db.ForeignKey("plantacoes.idPlantacao", ondelete='CASCADE'))
    medicao = db.relationship("Medicao")

    def __init__(self, codigo, tipo, idPlantacao):
        self.codigo = codigo
        self.tipo = tipo
        self.idPlantacao = idPlantacao

################################################## S C H E M A ##################################################
class SensorSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('idSensor', 'codigo', 'tipo', 'idPlantacao')

sensor_schema = SensorSchema()
sensores_schema = SensorSchema(many=True)

################################################## R O U T E S ##################################################
@app.route("/")
def sensor_homepage():
    text = "Este eh o backend do sistema de IoG - Internet of Gardens. Voce pode acessar os endpoints aqui descritos."

    response = {
        "status_code": 200,
        "message": text,
        "/sensor [POST]": "adiciona um sensor ao jardim",
        "/sensor [GET]": "retorna as informações de todos os sensores",
        "/sensor/<id> [GET]": "retorna as informações do sensor com o id especificado",
        "/sensor/<id> [PUT]": "atualiza as informações do sensor com o id especificado",
        "/sensor/<id> [DELETE]": "deleta o sensor com o id especificado",
    } 
    return jsonify(response)


# endpoint to create new line
@app.route("/sensor", methods=['POST'])
def add_sensor():
    if request.method == 'POST':
        codigo = request.json['codigo']
        tipo = request.json['tipo']
        idPlantacao = request.json['idPlantacao']

        new_sensor = Sensor(codigo, tipo, idPlantacao)
        db.session.add(new_sensor)
        db.session.commit()

        response = sensor_schema.dump(new_sensor)
        print("\n \n \n \n")
        print(response,type(response))
        print("\n \n \n \n")
        
        return jsonify(response)

# endpoint to show all lines
@app.route("/sensor", methods=['GET'])
def get_sensor():
    if request.method == 'GET':
        all_sensores = Sensor.query.all()
        
        response = sensores_schema.dump(all_sensores)
        
        return jsonify(response)

# endpoint to get line detail by id
@app.route("/sensor/<id>", methods=["GET"])
def sensor_detail(id):
    if request.method == 'GET':
        sensor = Sensor.query.get(id)
        response = sensor_schema.dump(sensor)

        return jsonify(response)

# endpoint to update line
# @app.route("/sensor/<id>", methods=["PUT"])
# def sensor_update(id):
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
@app.route("/sensor/<id>", methods=["DELETE"])
def sensor_delete(id):
    if request.method == 'DELETE':
        sensor = Sensor.query.get(id)
        if sensor is not None:
            db.session.delete(sensor)
            db.session.commit()

            return sensor_schema.jsonify(sensor)
        return None


############################################################################################################

if __name__ == '__main__':
    app.run(debug=True)