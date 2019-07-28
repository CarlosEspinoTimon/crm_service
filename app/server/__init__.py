"""
Server Module
"""
import sys

from flask import Flask
from flask import current_app
from flask import jsonify
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


sys.stdout.flush()
db = SQLAlchemy()
migrate = Migrate()


def create_app(app_config='config.Dev'):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object(app_config)

    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)

    # Import blueprints
    from .controller import customer_controller
    app.register_blueprint(customer_controller.customers)

    # A simple page that says server status
    @app.route('/')
    @cross_origin()
    def home():
        return jsonify('The server is running!!')

    return app
