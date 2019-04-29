#!/usr/bin/python3.6

from flask import Flask
from webapp import webappmain
from dbhelper import dbaccess

#api = Api(app)

def create_app(test_config = None):
    return webappmain.createapp(test_config)


if __name__ == '__main__':
    dbaccess.dbCreateIfNeeded()
    app = create_app()
    app.run(debug=True, host='0.0.0.0')

