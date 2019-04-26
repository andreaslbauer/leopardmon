#!/usr/bin/python3.6

# logging facility: https://realpython.com/python-logging/
import logging
import os
import pycouchdb

from leopardmontarget import testtarget

# create a sample test target object
def createSampleTestTargets() :
    code = """
response = requests.get(self.url)
print("HTTP Status Code: ", response.status_code, end='')
if (response.status_code == 200):
    status = 0
else:
    status = 1

"""
    url = "https://media.cellsignal.com/api/products/4060?country=JP"
    targetInfo = testtarget.TargetInfo("Japan Inventory and Pricing Microservice - SKU4060",
                                       code, url)
    return targetInfo


def main():

    # set up the logger
    logging.basicConfig(filename = "leopardmon.log", format='%(asctime)s %(levelname)s %(message)s',
                        level=logging.INFO)

    # log start up message
    logging.info("***************************************************************")
    logging.info("LeopardMon has started")
    logging.info("Working directory is %s", os.getcwd())

    couchDB = None
    couchDBServer = pycouchdb.Server()
    try:

        # create the couchdb instance - if it doesn't exist yet
        couchDB = couchDBServer.database("leopardmon-testtargets")
        logging.info("leopardmon-testargets DB successfully opened")

    except pycouchdb.exceptions.NotFound as e:
        couchDB = couchDBServer.create("leopardmon-testtargets")
        logging.info("leopardmon-testargets does not exist - create the DB")

    # read the target information records

    targetInfos = testtarget.TargetInfoDict()
    targetInfos.loadFromDB()

    if (targetInfos.len == 0):
        targetInfo = createSampleTestTargets()
        targetInfo.store()

    # loop through all targetinfo's and execute their tests
    for key, value in targetInfos.targetInfos.items():
        value.executeTest()

main()