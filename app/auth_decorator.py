from flask import session,render_template, request
from functools import wraps


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = dict(session).get('profile', None)
        # You would add a check here and usethe user id or something to fetch
        # the other data for that user/check if they exist
        if user:
            return f(*args, **kwargs)
        return render_template('sinLogueo.html', mensaje='Aun no has iniciado sesión')
        # return 'Aun no has iniciado sesión'
    return decorated_function