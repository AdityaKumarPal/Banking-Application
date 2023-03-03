from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = "************************"
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from bank import routes


"""
open python shell in terminal...
import os
os.urandom(12).hex()
************************
This key must be used in __init__.py for our registration form to be visible
"""
