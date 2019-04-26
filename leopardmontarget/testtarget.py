import sys
from io import StringIO
import io
import requests
import json

# logging facility: https://realpython.com/python-logging/
import logging
import pycouchdb


class TargetInfo:

    # default constructor- create empty object
    def __init__(self):
        self.name = ""
        self.testCode = ""
        self.lastStatus = 0
        self.url = ""

    # common constructor - initialize variables
    def __init__(self, name, testCode, url):
        self.name = name
        self.testCode = testCode
        self.lastStatus = 0
        self.url = url
        self._id = name

    def store(self):

        # get the couchDB server and instance
        # initialize global variable couch DB

        # create the couchdb instance - if it doesn't exist yet
        couchDBServer = pycouchdb.Server()
        couchDB = couchDBServer.database("leopardmon-testtargets")

        try:
            doc = None
            try:
                doc = couchDB.get(self.name)
                self._rev = doc["_rev"]
            except:
                pass

        except pycouchdb.exceptions.Conflict as e:
            pass

        doc = couchDB.save(self.__dict__)
        logging.info("Stored record %s", doc)

    # execute the check
    def executeTest(self):

        # create file-like string to capture output
        codeOut = io.StringIO()
        codeErr = io.StringIO()

        code = self.testCode

        # capture output and errors
        sys.stdout = codeOut
        sys.stderr = codeErr

        logging.info("Executing test code for: %s", self.name)
        try:
            exec(code)

        except Exception as e:
            logging.error("Error when executing code: %s", self.testCode)
            logging.error(e)
            self.lastStatus = 1

        else:

            logging.info("Test code outout: %s", codeOut.getvalue())
            logging.info("Test code errors: %s", codeErr.getvalue())
            self.lastStatus = 0

        finally:

            # restore stdout and stderr
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__

class TargetInfoDict :

    # default constructor- create empty object
    def __init__(self):
        self.targetInfos = {}

    # load the target info records from the CouchDB
    def loadFromDB(self):

        # get the database
        couchDBServer = pycouchdb.Server()
        couchDB = couchDBServer.database("leopardmon-testtargets")

        _viewdoc = {
            "_id": "listview",
            "views": {
                "names": {
                    "map": "function(doc) { emit(doc.name, 1); }",
                    "reduce": "function(k, v) { return  sum(v); }",
                    }
                }
            }

        viewdoc = couchDB.save(_viewdoc)
        docs = couchDB.query("listview", group='true')

        for doc in docs:
            print(doc)






