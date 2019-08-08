from functools import wraps
from flask import jsonify, request, current_app as app

from ..model.user import User

import jwt


def check_admin_token(func):
    @wraps(func)
    def decorated_funcion(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token:
            token = token.split('Bearer ')[1]
            payload, exception = process_token(token)
            if exception:
                return payload
            if payload.get('admin') is True:
                return func(*args, **kwargs)
            else:
                return jsonify('Forbidden'), 403
        else:
            return jsonify('Forbidden'), 403

    return decorated_funcion


def check_user_token(func):
    @wraps(func)
    def decorated_funcion(*args, **kwargs):
        token = request.headers.get('Authorization')
        if token:
            token = token.split('Bearer ')[1]
            payload, exception = process_token(token)
            if exception:
                return payload
            else:
                return func(*args, **kwargs)
        else:
            return jsonify('Forbidden'), 403

    return decorated_funcion


def process_token(token):
    try:
        payload = jwt.decode(
            token,
            app.config['SECRET_KEY'],
            algorithms=['HS256']
            )
    except jwt.ExpiredSignatureError:
        return jsonify('''Token expired'''), 401
    except jwt.InvalidSignatureError:
        return jsonify('''Signature verification failed'''), 401
    return payload, False
