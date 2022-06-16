import numpy as np
from flask import render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_user, LoginManager, login_required, logout_user
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Length, ValidationError
from models.db_setup import db_session
from models.entities import Role, UserAccount, Usertype, Image

from app import app
from app import bcrypt

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(phy_id):
    return db_session.query(UserAccount).get(int(phy_id))


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route("/", methods=['GET', 'POST'])
def index():
    roles = db_session.query(Role).all()
    return render_template('index.html', roles=roles)


class LoginForm(FlaskForm):
    login = StringField(validators=[
        InputRequired(), Length(min=4, max=20)], render_kw={"class": "form-control", "placeholder": "Login"})

    password = PasswordField(validators=[
        InputRequired(), Length(min=8, max=20)], render_kw={"class": "form-control","placeholder": "Password"})

    remember = BooleanField("remember me")


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db_session.query(UserAccount).filter_by(login=form.login.data).first()
        if user and bcrypt.check_password_hash(user.phyone_password, form.password.data):
            login_user(user)
            flash("you were just logged in!", "info")
            return redirect(url_for('dashboard'))
        else:
            flash("bad username or password")

    return render_template("login.html", form=form)


class RegisterForm(FlaskForm):
    login = StringField(validators=[
        InputRequired(), Length(min=4, max=20)], render_kw={"class": "form-control","placeholder": "Login"})

    email = StringField(validators=[
        InputRequired(), Length(min=4, max=20)], render_kw={"class": "form-control","placeholder": "Email"})

    password = PasswordField(validators=[
        InputRequired(), Length(min=8, max=20)], render_kw={"class": "form-control","placeholder": "Password"})

    submit = SubmitField('Register')

    def validate_login(self, user_login):
        existing_user_login = db_session.query(UserAccount).filter_by(login=user_login.data).first()
        if existing_user_login:
            raise ValidationError(
                'That login already exists. Please choose a different one.')


@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf8')

        user_token = str(np.random.randint(99999))
        new_usertype = Usertype(user_token=user_token, role_id=2)
        db_session.add(new_usertype)
        db_session.commit()

        usertype = db_session.query(Usertype).filter_by(user_token=user_token).first()
        new_user = UserAccount(login=form.login.data, phyone_password=hashed_password,
                               email=form.email.data,
                               subscription_=True,
                               user_id=usertype.user_id)

        db_session.add(new_user)
        db_session.commit()
        return redirect(url_for('login'))

    return render_template("register.html", form=form)


class DemoForm(FlaskForm):
    sex = SelectField('sex', choices=["man", "woman"])
    hair = SelectField('hair', choices=["long", "short"])
    eyes = SelectField('eyes', choices=["big", "small"])
    smile = SelectField('smile', choices=["normal", "happy", "sad"])
    face = SelectField('face', choices=["oval", "square", "round"])
    age = SelectField('age', choices=["young", "middle", "old"])
    nose = SelectField('nose', choices=["big", "small"])

    textInput = StringField(validators=[
        InputRequired()],
        render_kw={"placeholder": "enter the text description of the face"})

    submit = SubmitField('Demo')


@app.route('/demo', methods=['GET', 'POST'])
def demo():
    form = DemoForm()
    if request.method == "POST":
        data = {key: value for key, value in form.data.items() if key != "csrf_token"}
        return jsonify(data)
    return render_template('demo.html', form=form)


@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    return render_template('dashboard.html')


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    # path = "models/assets/mordor.png"
    user_type = db_session.query(Usertype).filter_by(user_id=5).first()
    user_image = db_session.query(Image).filter_by(fk_user_id=user_type.user_id).first()
    return render_template('profile.html', image=user_image.image_path)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))
