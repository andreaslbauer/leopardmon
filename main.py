#!/usr/bin/python3.6

# logging facility: https://realpython.com/python-logging/
import logging
import os
import pycouchdb

from leopardmontarget import testtarget


def main():

    # set up the logger
    logging.basicConfig(filename = "leopardmon.log", format='%(asctime)s %(levelname)s %(message)s',
                        level=logging.INFO)

    # log start up message
    logging.info("***************************************************************")
    logging.info("LeopardMon has started")
    logging.info("Working directory is %s", os.getcwd())


    # create the couchdb instance - if it doesn't exist yet
    couchDBServer = pycouchdb.Server()
    couchDB = couchDBServer.database("leopardmon-testtargets")

    try:

        logging.info("leopardmon-testargets DB successfully opened")

    except couchdb.http.ResourceNotFound as e:
        logging.info("leopardmon-testargets does not exist - create the DB")


    code = """
response = requests.get(self.url)
print("HTTP Status Code: ", response.status_code)
    """
    url = "https://media.cellsignal.com/api/products/4060?country=JP"

    targetInfo = testtarget.TargetInfo("Japan Inventory and Pricing Microservice",
                 code, url)

    # read the target information records


    targetInfo.executeTest()
    targetInfo.store()

    #targetInfo.store()

main()