from flask import Flask, url_for, redirect, sessions, render_template,request, make_response, flash
from authlib.integrations.flask_client import OAuth
import os

# decorator for routes that should be accessible only by logged in users
from app.auth_decorator import login_required

# dotenv setup
from dotenv import load_dotenv
load_dotenv()

from app import create_app
from app.forms import LoginForm

app = create_app()
# app = Flask(__name__)

# oAuth Setup
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id='470501504290-epn3ru4l5vbhp76rqo75j1023b6hvvd2.apps.googleusercontent.com',
    client_secret ='eFhUxigzSLBszO7ypWA1G8Ni',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'openid email profile'},
)

@app.route('/')
@login_required
def index():
    email = dict(session)['profile']['email']
    return f'Bienvenido a Google Drive, ingresaste como: {email}!'


@app.route('/login')
def login():
    google = oauth.create_client('google')  # create the google oauth client
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')  # create the google oauth client
    token = google.authorize_access_token()  # Access token from google (needed to get user info)
    resp = google.get('userinfo')  # userinfo contains stuff u specificed in the scrope
    user_info = resp.json()
    user = oauth.google.userinfo()
    session['profile'] = user_info
    session.permanent = True  # make the session permanant so it keeps existing after broweser gets closed
    return redirect('/')


@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html', error=error)


@app.errorhandler(500)
def server_error(error):
    return render_template('500.html', error=error)