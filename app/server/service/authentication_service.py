import json
import requests

from flask import url_for, current_app as app, request, jsonify
from oauthlib.oauth2 import WebApplicationClient

from ..model.user import User


class OAuthSignIn():
    providers = None
    client = None

    def __init__(self, provider_name):
        self.provider_name = provider_name
        credentials = app.config['OAUTH_CREDENTIALS'][provider_name]
        self.consumer_id = credentials.id
        self.consumer_secret = credentials.secret

    def authorize(self):
        pass

    def callback(self):
        pass

    def get_callback_url(self):
        return url_for('auth.oauth_callback', provider=self.provider_name,
                       _external=True)

    @classmethod
    def get_provider(cls, provider_name):
        if cls.client is None:
            cls.client = WebApplicationClient(app.config["GOOGLE_CLIENT_ID"])
        if cls.providers is None:
            cls.providers = {}
            for provider_class in cls.__subclasses__():
                provider = provider_class()
                cls.providers[provider.provider_name] = provider
        return cls.providers[provider_name]


class GoogleSignIn(OAuthSignIn):
    def __init__(self):
        super(GoogleSignIn, self).__init__('google')

    @classmethod
    def get_google_provider_cfg(cls):
        return requests.get(app.config["GOOGLE_DISCOVERY_URL"]).json()

    def authorize(self):
        # Find out what URL to hit for Google login
        google_provider_cfg = self.get_google_provider_cfg()
        authorization_endpoint = google_provider_cfg["authorization_endpoint"]

        # Use library to construct the request for Google login and provide
        # scopes that let you retrieve user's profile from Google
        request_uri = self.client.prepare_request_uri(
            authorization_endpoint,
            redirect_uri=request.base_url + "/callback",
            scope=["openid", "email", "profile"],
        )

        return jsonify({'uri': request_uri})

    def callback(self):
        # Get authorization code Google sent back to you
        code = request.args.get("code")

        # Find out what URL to hit to get tokens that allow you to ask for
        # things on behalf of a user
        google_provider_cfg = self.get_google_provider_cfg()
        token_endpoint = google_provider_cfg["token_endpoint"]

        # Prepare and send a request to get tokens! Yay tokens!
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
                app.config["GOOGLE_CLIENT_ID"],
                app.config["GOOGLE_CLIENT_SECRET"]
            ),
        )

        # Parse the tokens!
        self.client.parse_request_body_response(json.dumps(token_response.json()))


        # Now that you have tokens (yay) let's find and hit the URL
        # from Google that gives you the user's profile information,
        # including their Google profile image and email
        userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
        uri, headers, body = self.client.add_token(userinfo_endpoint)
        userinfo_response = requests.get(uri, headers=headers, data=body)

        # You want to make sure their email is verified.
        # The user authenticated with Google, authorized your
        # app, and now you've verified their email through Google!
        if userinfo_response.json().get("email_verified"):
            user_email = userinfo_response.json()["email"]
        else:
            return "User email not available or not verified by Google.", 400

        user = User.query.filter_by(email=user_email).first()
        if not user:
            return jsonify("User not stored")
        else:
            return user.generate_auth_token()
