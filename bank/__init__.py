from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = "0a2d48a71c19be41bdc3447c"
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from bank import routes
