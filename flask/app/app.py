import numpy as np
import torch
from flask import render_template, request, jsonify
from flask.app import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from tensorflow import Variable
from wtforms import SelectField

from models.db_setup import db_session
from models.entities import Role

import os

SECRET_KEY = os.urandom(32)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost:5432/gen_Imagedb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
app.config['SECRET_KEY'] = SECRET_KEY
db = SQLAlchemy(app)


class Form(FlaskForm):
    sex = SelectField('sex', choices=["man", "woman"])
    hair = SelectField('hair', choices=["long", "short"])
    eyes = SelectField('eyes', choices=["big", "small"])
    smile = SelectField('smile', choices=["normal", "happy", "sad"])
    face = SelectField('face', choices=["oval", "square", "round"])
    age = SelectField('age', choices=["young", "middle", "old"])
    nose = SelectField('nose', choices=["big", "small"])


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route("/", methods=['GET', 'POST'])
def index():
    form = Form()
    roles = db_session.query(Role).all()

    if request.method == "POST":
        data = {key: value for key, value in form.data.items() if key != "csrf_token"}
        return jsonify(data)

    return render_template('index.html', roles=roles, form=form)


@app.route("/home", methods=['GET', 'POST'])
def home():
    return render_template("new_index.html")


if __name__ == '__main__':
    # path = "../app/NN_module/model/image_encoder550.pth"
    # model = torch.load(path, map_location=torch.device("cuda"))
    # input_np = np.random.uniform(0, 1, (1, 10, 32, 32))
    # input_var = Variable(torch.FloatTensor(input_np))
    # k_model = pytorch_to_keras(model, input_var, [(10, None, None,)], verbose=True)

    # models.db_setup.init_db()
    app.run(host="0.0.0.0", debug=True)
