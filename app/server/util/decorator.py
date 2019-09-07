from functools import wraps
from flask import jsonify, request, current_app as app

from ..model.user import User

import jwt


def check_admin_token(func):
    @wraps(func)
    def decorated_funcion(*args, **kwargs):
        payload, error, kwargs = get_token_data(**kwargs)
        if error:
            return payload
        if payload.get('admin') is True:
            return func(*args, **kwargs)
        return jsonify('Forbidden'), 403

    return decorated_funcion


def check_user_token(func):
    @wraps(func)
    def decorated_funcion(*args, **kwargs):
        payload, error, kwargs = get_token_data(**kwargs)
        if error:
            return payload
        else:
            return func(*args, **kwargs)

    return decorated_funcion


def get_token_data(**kwargs):
    authorization_header = request.headers.get('Authorization')
    if authorization_header:
        token = authorization_header.split('Bearer ')[1]
        return process_token(token, **kwargs)
    else:
        return jsonify('Forbidden'), 403, None


def process_token(token, **kwargs):
    try:
        payload = jwt.decode(
            token,
            app.config['SECRET_KEY'],
            algorithms=['HS256']
        )
        kwargs = process_id_from_token(payload, **kwargs)
    except jwt.ExpiredSignatureError:
        return jsonify('''Token expired'''), 401, None
    except jwt.InvalidSignatureError:
        return jsonify('''Signature verification failed'''), 401, None
    except Exception as _:
        try:
            request.get_json()
        except Exception:
            return jsonify('''The request must have a body'''), 400, None
        return jsonify('''Signature verification failed'''), 401, None
    return payload, False, kwargs


def process_id_from_token(payload, **kwargs):
    if request.method == 'DELETE':
        kwargs['id_obtained_from_token'] = payload['id']
    elif request.method != 'GET':
        request.json['id'] = payload['id']
    return kwargs
