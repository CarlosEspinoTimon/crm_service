"""
Module
"""
import os
import sys
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask, jsonify, current_app
from flask_cors import CORS, cross_origin
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


sys.stdout.flush()


def create_app(app_config='config.Dev'):
    # create and configure the app
    app = Flask(__name__)
    app.config.from_object(app_config)

    cors = CORS(app)

    # A simple page that says server status
    @app.route('/')
    @cross_origin()
    def home():
        """
        Example of documentation endpoint
        :param string name: The name of foo
        :param int age: The age of foo
        :return: a text
        :rtype: string
        """
        return jsonify('The server is running!!')

    return app
