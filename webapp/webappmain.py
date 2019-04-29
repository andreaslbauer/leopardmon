from flask import Flask, render_template
import logging
import os
from . import auth
import pycouchdb


class TestResultList:

    # default constructor- create empty object
    def __init__(self):
        self.searchResults = list()

    # get our length
    @property
    def len(self):
        return self.searchResults.__len__()

    # load the target info records from the CouchDB
    def loadFromDB(self) -> object:

        # get the database
        couchDBServer = pycouchdb.Server()
        couchDB = couchDBServer.database("leopardmon-testresults")
        _viewDoc = None

        try:
            _viewDoc = couchDB.get("_design/listview")

        except pycouchdb.exceptions.NotFound as e:

            # view does exist - create it
            _viewdoc = {
                "_id": "_design/listview",
                "views": {
                    "names": {
                        "map": "function(doc) { emit(doc.name, 1); }",
                        "reduce": "function(k, v) { return  sum(v); }",
                    }
                }
            }

            viewdoc = couchDB.save(_viewdoc)

        # use the view to list all documents
        docnames = couchDB.query("listview/names", group='true')

        # load the targetinfo objects
        for docname in docnames:
            doc = couchDB.get(docname["key"])
            testResults = doc
            print(doc)
            self.searchResults.append(doc)



def getTestResults():
    # create the couchdb instance - if it doesn't exist yet

    testResultList = TestResultList()
    testResultList.loadFromDB()

    logging.info("Loading test results - got %i records", testResultList.len)

    return testResultList.searchResults


def createapp(test_config = None):
    # set up the logger
    logging.basicConfig(filename = "leopardapp.log", format='%(asctime)s %(levelname)s %(message)s',
                        level=logging.INFO)

    logging.info("Setting up Flask web app")

    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
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
        return render_template('home.html')

    @app.route('/dashboard')
    def dashboard():
        logging.info("HTTP GET for /dashboard")

        testResults = getTestResults()
        return render_template('dashboard.html', testResults = testResults)

    @app.route('/monitorlog')
    def monitorlog():
        logging.info("HTTP GET for /monitorlog")

        file = open("leopardmon.log", "r")
        lines = file.read()

        return render_template('monitorlog.html', lines=lines)

    app.register_blueprint(auth.bp)

    return app


