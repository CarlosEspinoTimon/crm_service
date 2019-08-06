from flask import Blueprint, jsonify, request
from flask_cors import CORS

from ..model.user import User

auth = Blueprint('auth', __name__, url_prefix='/auth')
CORS(auth, max_age=30*86400)


@auth.route('/login', methods=['POST'])
def login():
    """
    Function that given a email and a password as headers it checks if there
    is a user in the database and generates a token.
    """
    email = request.headers.get('email')
    password = request.headers.get('password')
    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        return jsonify('Token: {}'.format(user.generate_auth_token(1800)))
    else:
        return jsonify('Unauthorized'), 401
