from flask import Blueprint, jsonify, request
from flask_cors import CORS

from ..model.user import User

from ..service.authentication_service import OAuthSignIn


authentication = Blueprint('authentication', __name__, url_prefix='/login')
CORS(authentication, max_age=30 * 86400)


@authentication.route('', methods=['POST'])
def login():
    """
    .. http:post:: /login

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


@authentication.route('/<provider>')
def oauth_authorize(provider):
    """
    .. http:get:: /login/<provider>

    Function that given a provider from the available providers (google and
    facebook) it will return the uri to go to login with the third party OAuth
    provider.

    Return example:
        {
            "uri": "https://uri-of-provider"
        }

    :returns: The uri
    :rtype: dict

    """
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@authentication.route('/<provider>/callback')
def oauth_callback(provider):
    """
    .. http:get:: /login/<provider>/callback

    Callback endpoint that will be called after the user logs in with the third
    party OAuth provider. It will get the user eamil and check if it is in the
    system, generate a token and return it to the user.

    :returns: The token
    :rtype: String

    """
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.callback()
    
