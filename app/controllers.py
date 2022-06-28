import datetime
from functools import wraps
import jwt
import uuid
import jsonify
from flask import render_template, request, jsonify, redirect, url_for, flash, session
from flask_login import login_user, LoginManager, login_required, logout_user
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Length, ValidationError
from models.db_setup import db_session, photos
from models.entities import Role, UserAccount, Usertype, Image

from app import app
from app import bcrypt

login_manager = LoginManager()
login_manager.init_app(app)

# specific handler
login_manager.login_view = '/login'


@app.before_request
def make_session_permanent():
    session.permanent = True
    app.permanent_session_lifetime = datetime.timedelta(minutes=60)


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if session["token"] is not None:
            token = session["token"]

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")
            current_user = db_session.query(UserAccount).filter_by(phy_id=data['user_token']).first()
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated


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
        InputRequired(), Length(min=8, max=20)], render_kw={"class": "form-control", "placeholder": "Password"})

    remember = BooleanField("remember me")


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = db_session.query(UserAccount).filter_by(login=form.login.data).first()
        if user and bcrypt.check_password_hash(user.phyone_password, form.password.data):
            token = jwt.encode(
                {'user_token': user.phy_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                app.config["SECRET_KEY"])
            session["token"] = token
            login_user(user)
            flash("you were just logged in!", "info")
            return redirect(url_for('index'))
        else:
            flash("bad username or password")

    return render_template("login.html", form=form)


class RegisterForm(FlaskForm):
    login = StringField(validators=[
        InputRequired(), Length(min=4, max=20)], render_kw={"class": "form-control", "placeholder": "Login"})

    email = StringField(validators=[
        InputRequired(), Length(min=4, max=20)], render_kw={"class": "form-control", "placeholder": "Email"})

    password = PasswordField(validators=[
        InputRequired(), Length(min=8, max=20)], render_kw={"class": "form-control", "placeholder": "Password"})

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

        # user token id not just real token
        user_token = str(uuid.uuid4())
        new_usertype = Usertype(user_token=user_token, role_id=2)  # just user
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
    textInput = StringField(validators=[
        InputRequired()],
        render_kw={"min-width": "300px", "max-width": "500px", "placeholder": "введите текстовое описание лица"})

    submit = SubmitField('Demo')


@app.route('/demo', methods=['GET', 'POST'])
def demo():
    form = DemoForm()
    if request.method == "POST":
        text_input = form.data["textInput"]


        return jsonify(text_input)
    return render_template('demo.html', form=form)


@app.route('/profile', methods=['GET', 'POST'])
@login_required
@token_required
def profile(current_user):
    # path = "static/mordor.png" for DB pathname
    user_image = db_session.query(Image).filter_by(fk_user_id=current_user.user_id).all()
    image_path_list = [x.image_path for x in user_image]

    return render_template('profile.html', image=image_path_list, user_name=current_user.login)


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    session.pop('token')
    return redirect(url_for('login'))


@app.route('/save/image', methods=['GET', 'POST'])
# @login_required
def saveImage():
    image = None
    if request.method == "POST":
        file_name = photos.put(name="moscow.jpg",
                               path="static/moscow.jpg")

        # image = photos.get("mordor.png")

    return render_template('dashboard.html', image=image)
