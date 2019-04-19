import sys
from io import StringIO
import io
import requests
import json

# logging facility: https://realpython.com/python-logging/
import logging


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

        else:

            logging.info("Test code outout: %s", codeOut.getvalue())
            logging.info("Test code errors: %s", codeErr.getvalue())

        finally:

            # restore stdout and stderr
            sys.stdout = sys.__stdout__
            sys.stderr = sys.__stderr__

