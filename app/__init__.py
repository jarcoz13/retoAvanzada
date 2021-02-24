from flask import Flask, session
from flask_bootstrap import Bootstrap
from datetime import timedelta

from .config import Config

# from flask.ext.session import Session

def create_app():
    app = Flask(__name__)
    bootstrap = Bootstrap(app)
    # Session config
    app.config.from_object(Config)
    app.config['SECRET_KEY'] = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
    app.config['SESSION_COOKIE_NAME'] = 'google-login-session'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)
    app.config["SESSION_PERMANENT"] = False

    return app