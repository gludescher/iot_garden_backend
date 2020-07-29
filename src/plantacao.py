from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import Column, Integer, DateTime
from flask_cors import CORS
from garden_utils import *
import json 
import os
import datetime
import requests

################################################## M O D E L S ##################################################
class Plantacao(db.Model):
    __tablename__ = 'plantacoes'
    idPlantacao = db.Column(db.Integer, primary_key=True)
    planta = db.Column(db.String(80), unique=False)
    # tempMin = db.Column(db.Float(10), unique=False)
    # tempMax = db.Column(db.Float(10), unique=False)
    # umidMin = db.Column(db.Float(10), unique=False)
    # umidMax = db.Column(db.Float(10), unique=False)
    login = db.Column(db.Integer, db.ForeignKey('usuarios.login', ondelete='CASCADE'))
    sensor = db.relationship("Sensor")

    def __init__(self, planta, login):
        self.planta = planta
        # self.tempMin = tempMin
        # self.tempMax = tempMax
        # self.umidMin = umidMin
        # self.umidMax = umidMax
        self.login = login

################################################## S C H E M A ##################################################
class PlantacaoSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('idPlantacao', 'planta', 'login')

plantacao_schema = PlantacaoSchema()
plantacoes_schema = PlantacaoSchema(many=True)

################################################## R O U T E S ##################################################
@app.route("/")
def plantacao_homepage():
    text = "Este eh o backend do sistema de IoG - Internet of Gardens. Voce pode acessar os endpoints aqui descritos."

    response = {
        "status_code": 200,
        "message": text,
        "/plantacao [POST]": "adiciona uma plantacao ao evento",
        "/plantacao [GET]": "retorna as informacoes de todas as plantacoes",
        "/plantacao/<id> [GET]": "retorna as informacoes da plantacao com o id especificado",
        "/plantacao/<id> [PUT]": "atualiza as informacoes da plantacao com o id especificado",
        "/plantacao/<id> [DELETE]": "deleta a plantacao com o id especificado",
    } 
    return jsonify(response)


# endpoint to create new line
@app.route("/plantacao", methods=['POST'])
def add_plantacao():
    if request.method == 'POST':
        login = request.json['login']
        planta = request.json['planta']
        # tempMin = request.json['tempMin']
        # tempMax = request.json['tempMax']
        # umidMin = request.json['umidMin']
        # umidMax = request.json['umidMax']

        new_plantacao = Plantacao(planta, login)
        db.session.add(new_plantacao)
        db.session.commit()

        response = plantacao_schema.dump(new_plantacao)
        print("\n \n \n \n")
        print(response,type(response))
        print("\n \n \n \n")
        
        return jsonify(response)

# endpoint to show all lines
@app.route("/plantacao", methods=['GET'])
def get_plantacao():
    if request.method == 'GET':
        all_plantacoes = Plantacao.query.all()
        
        response = plantacoes_schema.dump(all_plantacoes)
        
        return jsonify(response)

# endpoint to get line detail by id
@app.route("/plantacao/<id>", methods=["GET"])
def plantacao_detail(id):
    if request.method == 'GET':
        plantacao = Plantacao.query.get(id)
        response = plantacao_schema.dump(plantacao)

        return jsonify(response)

# endpoint to update line
@app.route("/plantacao/<id>", methods=["PUT"])
def plantacao_update(id):
    if request.method == 'PUT':

        plantacao = Plantacao.query.get(id)

        if plantacao is not None:
            if 'nome' in request.json.keys():
                plantacao.nome = request.json['nome']
            if 'senha' in request.json.keys():
                plantacao.senha = request.json['senha']
            
            db.session.commit()

            return plantacao_schema.jsonify(plantacao)

        return None

# endpoint to delete line
@app.route("/plantacao/<id>", methods=["DELETE"])
def plantacao_delete(id):
    if request.method == 'DELETE':
        plantacao = Plantacao.query.get(id)
        if plantacao is not None:
            db.session.delete(plantacao)
            db.session.commit()

            return plantacao_schema.jsonify(plantacao)
        return None


############################################################################################################