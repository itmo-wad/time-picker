"""
App initialization file.
Imports and initializes its main components.
"""

import os
from flask import Flask
from config import Config 			# Project configuration import
from flask_pymongo import PyMongo


# Create Flask app, load app.config
app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.environ.get("SECRET_KEY")


# MongoDB
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
mongo = PyMongo(app)

import views
