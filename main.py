from flask import Flask, url_for, redirect, sessions, render_template
from authlib.integrations.flask_client import OAuth
import os
from datetime import timedelta

# decorator for routes that should be accessible only by logged in users
from auth_decorator import login_required

# dotenv setup
# from dotenv import load_dotenv
# load_dotenv()


app = Flask(__name__)

# Session config
app.secret_key = ("APP_SECRET_KEY")
# app.secret_key = os.getenv("APP_SECRET_KEY")
app.config['SESSION_COOKIE_NAME'] = 'google-login-session'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)


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
def hello_word():
    email = dict(session)['profile']['email']
    return f'Bienvenido a Google Drive, ingresaste como: {email}!'


@app.route('/login')
def login():
    google = oauth.create_client('google')
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    # resp = google.get('account/verify_credentials.json')
    resp = google.get('userinfo')
    info_user = resp.json()
    user = oauth.google.userinfo()
    # do something with the token and profile
    # session['email'] = user_info['email']
    session['profile'] = info_user
    session.permanent = True
    return redirect('/')


@app.route('/logout')
def logout():
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')

