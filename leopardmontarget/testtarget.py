import sys
from io import StringIO
import io
import requests
import json
import datetime

# logging facility: https://realpython.com/python-logging/
import logging
import pycouchdb


class TargetInfo:

    # common constructor - initialize variables
    def __init__(self, name = "", testCode = "", url = ""):
        self.name = name
        self.testCode = testCode
        self.lastStatus = 0
        self.url = url
        self._id = name

    # class method - create from value dict
    @classmethod
    def createFromDict(cls, valuedict: object) -> object:
        clsinstance = cls()
        clsinstance.__dict__ = valuedict
        clsinstance.lastStatus = 0
        return clsinstance

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

        # execute the test code
        code = self.testCode


        # capture output and errors
        sys.stdout = codeOut
        sys.stderr = codeErr
        elapsedtime = 0
        status = 0
        starttime = datetime.datetime.now()

        logging.info("Executing test code for: %s", self.name)
        try:
            exec(code)
            self.laststatus = status

        except Exception as e:
            logging.error("Error when executing check: %s", self.name)
            logging.error(e)
            self.lastStatus = 1

        else:

            codeOutValue = codeOut.getvalue()
            codeErrValue = codeErr.getvalue()
            if (len(codeOutValue) > 0):
                logging.info("Test code outout: %s", codeOutValue)
            if (len(codeErrValue) > 0):
                logging.info("Test code errors: %s", codeErrValue)
            self.lastStatus = 0

        finally:

            # restore stdout and stderr
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__

        endtime = datetime.datetime.now()
        elapsedtime = (endtime - starttime).total_seconds() * 1000

        logging.info("Executed check %s in %i ms with status %i", self.name, elapsedtime, self.lastStatus)

class TargetInfoDict :

    # default constructor- create empty object
    def __init__(self):
        self.targetInfos = {}

    # get our length
    @property
    def len(self):
        return self.targetInfos.__len__()

    # load the target info records from the CouchDB
    def loadFromDB(self):

        # get the database
        couchDBServer = pycouchdb.Server()
        couchDB = couchDBServer.database("leopardmon-testtargets")
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
            targetInfo = TargetInfo.createFromDict(doc)
            self.targetInfos[targetInfo.name] = targetInfo






