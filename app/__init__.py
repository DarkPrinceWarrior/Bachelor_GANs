import os
from flask_bcrypt import Bcrypt
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config

SECRET_KEY = os.urandom(32)


app = Flask(__name__)
bcrypt = Bcrypt(app)
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://postgres:{config.password}' \
                                        f'@localhost:{config.port}/{config.db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.config['SECRET_KEY'] = SECRET_KEY
db = SQLAlchemy(app)

from app import controllers





