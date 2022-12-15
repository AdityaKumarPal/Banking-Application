from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = "566ddd84f005ac3d58fa5db2"
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from bank import routes

