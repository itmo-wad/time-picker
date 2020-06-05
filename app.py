"""
App initialization file.
Imports and initializes its main components.
"""

import os
from flask import Flask
from config import Config 				# Project configuration import
from flask_bcrypt import Bcrypt 		# Module for password hashing
from flask_pymongo import PyMongo 		# PyMongo database
from flask_login import LoginManager	# User sessions and etc.


# Create Flask app, load app.config
app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = b'eHk\x8d\xd9\x18\xf1\xd9)#\xaaf\x8aK=<'#os.environ.get("SECRET_KEY")

# PyMongo DB initialization
mongo = PyMongo(app)
# Bcrypt initialization
bcrypt = Bcrypt(app)
# LoginManager initialization
login_manager = LoginManager(app)
# Default function, when @login_required decorator is used
login_manager.login_view = 'login'
# Bootstrap4 style for displayed flash message
login_manager.login_message_category = 'info'


import views
