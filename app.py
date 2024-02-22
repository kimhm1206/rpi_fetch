from flask import Flask,request
from flask_restx import Resource, Api
from uploadWeather import Weather
import json


app = Flask(__name__)
api = Api(app)

api.add_namespace(Weather, '/weatherstation/')



if __name__ == '__main__':
    app.run(host='192.168.5.1',port = 8080)
