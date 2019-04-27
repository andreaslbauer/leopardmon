#!/usr/bin/python3.6

from flask import Flask
import logging
from mailhelper import mailhelper
from monitor import leopardmon
import threading
import os

def create_app(test_config = None):

    # set up the logger
    logging.basicConfig(filename = "leopardmon.log", format='%(asctime)s %(levelname)s %(message)s',
                        level=logging.INFO)

    logging.info("Setting up Flask web app")

    # create and configure the app
    app = Flask(__name__, instance_relative_config = True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass


    logging.info("Setting up Flask routes")

    # a simple page that says hello
    @app.route('/')
    def home():
        logging.info("HTTP GET for /")
        return 'Homepage!'

    @app.route('/hello')
    def home():
        logging.info("HTTP GET for /hello")
        return 'Hello!'

    return app



create_app()
