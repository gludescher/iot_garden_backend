from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS, cross_origin
import json 
import os
import datetime
import requests
import serial

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

class DataReceiver(): 
    #Configurações da Porta Serial
    def __init__(self):
        self.arduino = serial.Serial()
        self.arduino.port = "COM2"

        #Tempo de aguardo por uma resposta do arduino em segundos antes de encerrar conexao
        #Tem que ser maior entre o delay de envio de informacoes do sensores
        self.arduino.timeout = 20

        #Dict de medicoes
        self.medicoes = {}

    def close(self):
        self.arduino.close()
    
    def open(self):
        self.arduino.open()

    def build_dict(self, sensor_name): 
        sensor = {}
        sensor["namePlant"] = sensor_name
        sensor["temperatureAir"] = "Inativo"
        sensor["humidityAir"] = "Inativo"
        sensor["humiditySoil"] = "Inativo"
        return sensor

    def format_data(self, string_serial):
        string_parser = string_serial.split(':')
        sensor_name = string_parser[0]
        sensor_values = string_parser[1]
        sensor_values = sensor_values.split(',')

        sensor = self.build_dict(sensor_name)

        for value in sensor_values:
            value_parser = value.split('=')
            if value_parser[0] == "temperatureAir":
                if float(value_parser[1]) > 0:
                    sensor["temperatureAir"] = "Ativo"
            if value_parser[0] == "humidityAir":
                if float(value_parser[1]) > 20:
                    sensor["humidityAir"] = "Ativo"
            if value_parser[0] == "humiditySoil":
                if float(value_parser[1]) > 0:
                    sensor["humiditySoil"] = "Ativo"

        self.medicoes[sensor_name] = sensor

    def receive_data(self):
        string_serial = str(self.arduino.readline())
        string_serial = string_serial.replace("b'", "")
        string_serial = string_serial[:-5]
        self.format_data(string_serial)

        return string_serial
    
################################################## R O U T E S ##################################################
@app.route("/")
def homepage():

    response = {
        "/unknown_sensors [GET]": "retrieve all new sensors installed"
    } 
    return jsonify(response)


# endpoint to create new line
@app.route("/unknown_sensors", methods=['GET'])
@cross_origin(origin='*')
def get_fila():
    if request.method == 'GET':
        data_receiver = DataReceiver() 
        data_receiver.close()
        data_receiver.open()
        while True:
            data_receiver.receive_data()
            if len(data_receiver.medicoes.keys()) > 0:
                break
        
        return jsonify(data_receiver.medicoes)
                
############################################################################################################

if __name__ == '__main__':
    app.run(debug=True)