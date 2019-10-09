"""
Server Module
"""
import sys

from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_marshmallow import Marshmallow


sys.stdout.flush()
db = SQLAlchemy()
migrate = Migrate()
ma = Marshmallow()


def create_app(app_config):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object(app_config)

    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)
    ma.init_app(app)

    from .model.customer import Customer
    from .model.user import User

    # Import blueprints
    from .controller import customer_controller
    app.register_blueprint(customer_controller.customers)
    from .controller import user_controller
    app.register_blueprint(user_controller.users)
    from .controller import auth_controller
    app.register_blueprint(auth_controller.auth)

    # A simple page that says server status
    @app.route('/')
    def home():
        return jsonify('The server is running!!')

    return app
