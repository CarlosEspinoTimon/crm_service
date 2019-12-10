import json
import requests

from flask import current_app as app, request, jsonify
from oauthlib.oauth2 import WebApplicationClient

from ..model.user import User

def basic_login():
    email = request.headers.get('email')
    password = request.headers.get('password')
    user = User.query.filter_by(email=email).first()

    if user and user.check_password(password):
        return jsonify('Token: {}'.format(user.generate_auth_token(1800)))
    else:
        return jsonify('Unauthorized'), 401


class OAuthSignIn():
    providers = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = app.config['OAUTH_CREDENTIALS'][provider_name]
        self.consumer_id = credentials.id
        self.consumer_secret = credentials.secret

    def authorize(self):
        pass

    def callback(self):
        pass

    def check__for_user_in_database(self, email):
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify('Forbidden'), 403
        else:
            return jsonify('Token: {}'.format(user.generate_auth_token(1800)))

    @classmethod
    def get_provider(cls, provider_name):
        if cls.providers is None:
            cls.providers = {}
            for provider_class in cls.__subclasses__():
                provider = provider_class()
                cls.providers[provider.provider_name] = provider
        return cls.providers[provider_name]


class GoogleSignIn(OAuthSignIn):

    def __init__(self):
        super(GoogleSignIn, self).__init__('google')
        self.client = WebApplicationClient(self.consumer_id)

    @classmethod
    def get_google_provider_cfg(cls):
        return requests.get(app.config["GOOGLE_DISCOVERY_URL"]).json()

    def authorize(self):
        google_provider_cfg = self.get_google_provider_cfg()
        authorization_endpoint = google_provider_cfg["authorization_endpoint"]

        request_uri = self.client.prepare_request_uri(
            authorization_endpoint,
            redirect_uri=request.base_url + "/callback",
            scope=["openid", "email", "profile"],
        )

        return jsonify({'uri': request_uri})

    def callback(self):
        code = request.args.get("code")

        google_provider_cfg = self.get_google_provider_cfg()
        token_endpoint = google_provider_cfg["token_endpoint"]

        token_url, headers, body = self.client.prepare_token_request(
            token_endpoint,
            authorization_response=request.url,
            redirect_url=request.base_url,
            code=code
        )
        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(
                self.consumer_id,
                self.consumer_secret
            ),
        )

        self.client.parse_request_body_response(
            json.dumps(token_response.json())
        )

        userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
        uri, headers, body = self.client.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body)

        if userinfo_response.json().get("email_verified"):
            user_email = userinfo_response.json()["email"]
        else:
            return jsonify("User email not available or not verified by Google."), 400

        return super().check__for_user_in_database(user_email)


class FacebookSignIn(OAuthSignIn):

    def __init__(self):
        super(FacebookSignIn, self).__init__('facebook')
        self.client = WebApplicationClient(self.consumer_id)
        self.authorize_url = app.config["FACEBOOK_AUTHORIZE_URL"]
        self.access_token_url = app.config["FACEBOOK_ACCESS_TOKEN_URL"]
        self.user_info_url = app.config["FACEBOOK_USER_INFO_URL"]

    def authorize(self):
        request_uri = self.client.prepare_request_uri(
            self.authorize_url,
            redirect_uri=request.base_url + "/callback",
            scope=["email"],
        )

        return jsonify({'uri': request_uri})

    def callback(self):
        code = request.args.get("code")

        token_url, headers, body = self.client.prepare_token_request(
            self.access_token_url,
            authorization_response=request.url,
            redirect_url=request.base_url,
            code=code
        )
        token_response = requests.post(
            token_url,
            headers=headers,
            data=body,
            auth=(
                self.consumer_id,
                self.consumer_secret
            ),
        )

        self.client.parse_request_body_response(
            json.dumps(token_response.json())
        )

        uri, headers, body = self.client.add_token(self.user_info_url)
        userinfo_response = requests.get(uri, headers=headers, data=body)

        user_email = userinfo_response.json()["email"]

        return super().check__for_user_in_database(user_email)
