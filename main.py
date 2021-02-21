from flask import Flask, url_for, redirect, sessions, render_template
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key= 'random secret'

oauth = OAuth(app)

google = oauth.register(
    name= 'google',
    client_id='470501504290-epn3ru4l5vbhp76rqo75j1023b6hvvd2.apps.googleusercontent.com',
    client_secret ='eFhUxigzSLBszO7ypWA1G8Ni',
    access_token_url = 'https://accounts.google.com/o/oauth2/token',
    access_token_params = None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url = 'https://www.googleapis.com/oauth2/v1/',
    client_lowargs = {'scope': 'openid profile email'},
)

@app.route('/')
def hello_word():
    email = dict(session).get('email', None)
    return 'Bienvenido {email}'.format(email)


@app.route('/login')
def login():
    google = oauth.create_client('google')
    redirect_uri = url_for('authorize', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    google = oauth.create_client('google')
    token = google.authorize_access_token()
    resp = google.get('account/verify_credentials.json')
    profile = resp.json()
    # do something with the token and profile
    session['email'] = user_info['email']
    return redirect('/')