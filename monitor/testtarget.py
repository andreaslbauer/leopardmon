import sys
from io import StringIO
import io
import requests
import json
import datetime
from mailhelper import mailhelper
# logging facility: https://realpython.com/python-logging/
import logging
import pycouchdb


class TargetInfo:

    # common constructor - initialize variables
    def __init__(self, name = "", testCode = "", url = "", runInterval = 30):
        self.name = name
        self.testCode = testCode
        self.lastStatus = 0
        self.url = url
        self.runInterval = runInterval
        self.runCountdown = 0
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
        #logging.info("Stored target info record: %s", doc)

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
            body = self.name + "\r\n" + str(e)
            mailhelper.sendMail("andreas.bauer@cellsignal.com", "Webproperty Monitor Alert", body)
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

        # store the results
        testResult = TestResult.updateTestResults(self, status, lastTimeElapsed = elapsedtime)
        testResult.store()

class TargetInfoDict :

    # default constructor- create empty object
    def __init__(self):
        self.targetInfos = {}

    # get our length
    @property
    def len(self):
        return self.targetInfos.__len__()

    # load the target info records from the CouchDB
    def loadFromDB(self) -> object:

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


class TestResult:

    # common constructor - initialize variables
    def __init__(self, name = "", url = "", lastTested = None, lastStatus = 0, lastSuccess = None, lastFailure = None, lastTimeElapsed = 0):
        self.name = name
        self.url = url
        self.lastTested = None
        self.lastStatus = 0
        self.lastSuccess = None
        self.lastFailure = None
        self.lastTimeElapsed = lastTimeElapsed
        self._id = name
        self.results = list()

    def store(self):
        # get the couchDB server and instance
        # initialize global variable couch DB

        # create the couchdb instance - if it doesn't exist yet
        couchDBServer = pycouchdb.Server()
        couchDB = couchDBServer.database("leopardmon-testresults")

        try:
            doc = None
            try:
                doc = couchDB.get(self.name)
                self._rev = doc["_rev"]
            except:
                pass

        except pycouchdb.exceptions.NotFound as e:
            pass

        # update the date/time stamps
        now = datetime.datetime.now()
        nowDateTimeStr = now.strftime("%Y-%m-%d %H:%M:%S")

        self.lastTested = nowDateTimeStr
        if (self.lastStatus > 0):
            self.lastFailure = nowDateTimeStr

        else:
            self.lastSuccess = nowDateTimeStr

        resultTuple = {}
        resultTuple["datetime"] = nowDateTimeStr
        resultTuple["status"] = self.lastStatus
        resultTuple["timeelapsed"] = self.lastTimeElapsed

        results = list()
        results.append(resultTuple)
        if (doc != None):
            results = results + doc["results"][0:63]

        self.results = results

        doc = couchDB.save(self.__dict__)
        #logging.info("Stored test results record: %s", doc)

    # class method - create and store test results
    @classmethod
    def updateTestResults(cls, testTarget, status, lastTimeElapsed):
        clsinstance = cls()
        clsinstance.lastStatus = status
        clsinstance.name = testTarget.name
        clsinstance._id = testTarget.name
        clsinstance.url = testTarget.url
        clsinstance.lastTimeElapsed = lastTimeElapsed

        return clsinstance



