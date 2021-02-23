from flask import Flask
from flask_bootstrap import Bootstrap
from datetime import timedelta

from .config import Config


def create_app():
    app = Flask(__name__)
    bootstrap = Bootstrap(app)
    # Session config
    app.secret_key = ("APP_SECRET_KEY")
    app.config.from_object(Config)
    app.config['SESSION_COOKIE_NAME'] = 'google-login-session'
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

    return app