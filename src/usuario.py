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
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    # idUsuario = db.Column(db.Integer,)
    login = db.Column(db.String(30), unique=True, primary_key=True)
    nome = db.Column(db.String(80), unique=False)
    plantacao = db.relationship('Plantacao', backref='usuarios', lazy='dynamic')
    # sensor = db.relationship("Sensor", foreign_key=idUsuario)

    def __init__(self, nome, login):
        self.nome = nome
        self.login = login

################################################## S C H E M A ##################################################
class UsuarioSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('nome', 'login')

usuario_schema = UsuarioSchema()
usuarios_schema = UsuarioSchema(many=True)

################################################## R O U T E S ##################################################
@app.route("/")
def usuario_homepage():
    text = "Este eh o backend do sistema de IoG - Internet of Gardens. Voce pode acessar os endpoints aqui descritos."

    response = {
        "status_code": 200,
        "message": text,
        "/usuario [POST]": "adiciona um usuario ao sistema",
        "/usuario [GET]": "retorna as informacoes de todos os usuarios",
        "/usuario/<id> [GET]": "retorna as informacoes do usuario com o id especificado",
        "/usuario/<id> [PUT]": "atualiza as informacoes do usuario com o id especificado",
        "/usuario/<id> [DELETE]": "deleta o usuario com o id especificado",
    } 
    return jsonify(response)
    


# endpoint to create new line
@app.route("/usuario", methods=['POST'])
def add_usuario():
    if request.method == 'POST':
        nome = request.json['nome']
        login = request.json['login']
        
        new_usuario = Usuario(nome, login)
        return synchronous_db_insert(object=new_usuario, object_schema=usuario_schema, path='usuarios') 

# endpoint to show all lines
@app.route("/usuario", methods=['GET'])
def get_usuario():
    if request.method == 'GET':
        all_usuarios = Usuario.query.all()
        
        response = usuarios_schema.dump(all_usuarios)
        
        return jsonify(response)

@app.route("/usuario/nome/<nome_busca>", methods=['GET'])
def get_usuario_by_name(nome_busca):
    if request.method == 'GET':
        print(nome_busca)
        usuarios = Usuario.query.filter(Usuario.nome.like("%"+nome_busca+"%"))
        
        response = usuarios_schema.dump(usuarios)
        
        return jsonify(response)

# endpoint to get line detail by id
@app.route("/usuario/<id>", methods=["GET"])
def usuario_detail(id):
    if request.method == 'GET':
        usuario = Usuario.query.get(id)
        response = usuario_schema.dump(usuario)

        return jsonify(response)

# endpoint to update line
@app.route("/usuario/<id>", methods=["PUT"])
def usuario_update(id):
    if request.method == 'PUT':

        usuario = Usuario.query.get(id)

        if usuario is not None:
            if 'nome' in request.json.keys():
                usuario.nome = request.json['nome']
            
            db.session.commit()

            return usuario_schema.jsonify(usuario)

        return None

# endpoint to delete line
@app.route("/usuario/<id>", methods=["DELETE"])
def usuario_delete(id):
    if request.method == 'DELETE':
        usuario = Usuario.query.get(id)
        if usuario is not None:
            db.session.delete(usuario)
            db.session.commit()

            return usuario_schema.jsonify(usuario)
        return None


############################################################################################################