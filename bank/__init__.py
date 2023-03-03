from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = "************************"
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from bank import routes

<<<<<<< HEAD
"""
For Secret_Key used above...
open python shell in terminal...
import os
os.urandom(12).hex()
0a2d48a71c19be41bdc3447c
=======

"""
open python shell in terminal...
import os
os.urandom(12).hex()
************************
>>>>>>> master
This key must be used in __init__.py for our registration form to be visible
"""
