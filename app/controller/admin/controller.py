import os
import pathlib
import requests

from flask import request, render_template, redirect, url_for, session, abort, flash
from flask.helpers import url_for
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests

from . import admin

from app.models.facultyModel import facultyModel
from app.models.adminModel import AdminUser
from app.controller.admin.forms import AdminLoginForm

from flask import flash
from flask_login import login_user, current_user, login_required, logout_user
from flask_login import LoginManager, UserMixin

facultyModel = facultyModel()

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

GOOGLE_CLIENT_ID = (
    "499940727103-5q18al7g2749q5joa1mbr6fjrapb03qn.apps.googleusercontent.com"
)
client_secrets_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secrets_file,
    scopes=[
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
        "openid",
    ],
    redirect_uri="http://127.0.0.1:8080/callback",
)


def login_is_required(function):
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            return abort(401)  # Authorization required
        else:
            return function()

    return wrapper


@admin.route("/")
def index():
    if "google_id" in session:
        return render_template("home.html")
    else:
        return render_template("login.html")



@admin.route("/login")
def login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)

@admin.route("/adminLogin", methods=['GET', 'POST'])
def adminLogin():
    form = AdminLoginForm()

    if request.method == 'POST' and form.validate_on_submit():
        user_email = form.adminEmail.data
        user_password = form.adminPassword.data

        if user_email == "admin@g.msuiit.edu.ph" and user_password == "admin":
            # Log in the user using Flask-Login
            admin_user = AdminUser(user_id="admin", email=user_email, role="Admin")
            login_user(admin_user)

            session['google_id'] = "admin"
            session['name'] = "Admin"
            session['email'] = user_email
            session['role'] = "Admin"

            flash("Login successful", "success")
            # return redirect(url_for('admin.login'))
            return redirect(url_for('admin.wrapper'))
            # return render_template('adminTest.html')
        else:
            flash("Invalid email or password", "danger")

    return render_template("admin_login.html", form=form)

@admin.route("/callback")
def callback():
    flow.fetch_token(authorization_response=request.url)

    # if not session["state"] == request.args["state"]:
    #     abort(500)

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token, request=token_request, audience=GOOGLE_CLIENT_ID
    )
    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    session["email"] = id_info.get("email")
    facultyRole = facultyModel.get_facultyRole(session.get("email"))
    session["role"] = facultyRole[0]["role"]

    user_info_endpoint = "https://www.googleapis.com/oauth2/v1/userinfo"
    user_info_response = requests.get(
        user_info_endpoint, headers={"Authorization": "Bearer " + credentials.token}
    )
    user_info = user_info_response.json()

    session["profile_picture"] = user_info.get("picture")

    if session["email"] == "admin@g.msuiit.edu.ph":
        user = AdminUser()
        user.id = session["google_id"]
        user.name = session["name"]
        user.email = session["email"]
        user.role = session["role"]

        login_user(user)

    return redirect("/home")


@admin.route("/logout")
def logout():
    session.clear()
    logout_user()
    return redirect("/")


@admin.route("/home")
@login_is_required
def protected_area():
    return render_template("home.html")
