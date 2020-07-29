from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from sqlalchemy import Column, Integer, DateTime
from flask_cors import CORS
from garden_utils import app, db
import json 
import os
import datetime
import requests
from threading import Thread
from usuario import Usuario
from plantacao import Plantacao
from sensor import Sensor
from medicao import Medicao, get_unposted_medicoes
import time
import atexit

threads = []

def post_medicoes_thread(wait=30):
    print(" Thread para POST de medições iniciada ".center(80, '='))
    time.sleep(wait)
    while True:
        time.sleep(wait)
        medicoes = get_unposted_medicoes()
        print(datetime.datetime.now())
        print(medicoes)
        
        # print("I'm a new kinda thread around here")

# def thread_dummy(wait=15):
#     print(" Thread DUMMY iniciada ".center(80, '='))
#     while True:
#         # medicoes = medicao.get_unposted_medicoes()
#         time.sleep(wait)
#         print(" Mom says I'm a very special boy heh")

def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        print("Oopsy, I messed up")
        raise RuntimeError('Not running with the Werkzeug Server')
    func()
    print("Bye, guys...")

@app.route("/shutdown", methods=['POST'])
def shutdown():
    shutdown_server()
    return "Server shutting down... Bye friend... :c"

# atexit.register(close_running_threads)  

if __name__ == '__main__':
    print(" Aquecendo os motores!!! ".center(90, '='))
    # t1 = Thread(target=post_medicoes_thread, daemon=True)
    # t1.start()
    # threads.append(t1)
    db.create_all()
    app.run(debug=True, port=5001)


