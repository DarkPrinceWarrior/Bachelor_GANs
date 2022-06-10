from flask import render_template, request, jsonify
from flask.app import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
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


if __name__ == '__main__':
    # models.db_setup.init_db()
    app.run(host="0.0.0.0", debug=True)
