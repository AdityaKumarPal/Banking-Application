from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = "566ddd84f005ac3d58fa5db2"
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from bank import routes

"""
For Secret_Key used above...
open python shell in terminal...
import os
os.urandom(12).hex()
0a2d48a71c19be41bdc3447c
This key must be used in __init__.py for our registration form to be visible
"""
