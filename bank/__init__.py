from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = "*******************"
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from bank import routes


"""
For Secret key used above, open terminal and follow below process.
import os
os.urandom(12).hex()
*********************
The above key must be used in app.config["SECRET_KEY"]
"""
