import logging
import os
import pycouchdb
import time
from monitor import testtarget

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
    url = "https://media.cellsignal.com/api/products/4370?country=JP"
    targetInfo = testtarget.TargetInfo("Japan Inventory and Pricing Microservice - SKU4370",
                                       code, url, runInterval = 10)
    targetInfo.store()

    url = "https://media.cellsignal.com/api/products/4060?country=JP"
    targetInfo = testtarget.TargetInfo("Japan Inventory and Pricing Microservice - SKU4060",
                                       code, url, runInterval = 10)
    targetInfo.store()

    url = "http://www.cellsignal.com"
    targetInfo = testtarget.TargetInfo("Homepage www.cellsignal.com",
                                       code, url, runInterval = 10)
    targetInfo.store()

    url = "http://www.cellsignal.de"
    targetInfo = testtarget.TargetInfo("Homepage www.cellsignal.de",
                                       code, url, runInterval = 10)
    targetInfo.store()

    url = "http://www.cellsignal.jp"
    targetInfo = testtarget.TargetInfo("Homepage www.cellsignal.jp",
                                       code, url, runInterval = 10)
    targetInfo.store()

    url = "http://cst-c.com.cn"
    targetInfo = testtarget.TargetInfo("Homepage www.cst-c.com.cn",
                                       code, url, runInterval = 10)
    targetInfo.store()



    return targetInfo

# *******************************************************************
# check whether the CouchDBs and also the initial documents exist
# if they don't exist create them
# *******************************************************************

def createDBDocumentsIfNeeded():
    couchDB = None
    couchDBServer = pycouchdb.Server()
    try:

        # create the couchdb instance - if it doesn't exist yet
        couchDB = couchDBServer.database("leopardmon-testtargets")
        logging.info("leopardmon-testargets DB successfully opened")

    except pycouchdb.exceptions.NotFound as e:
        couchDB = couchDBServer.create("leopardmon-testtargets")
        logging.info("leopardmon-testargets does not exist - create the DB")

    try:

        # create the couchdb instance - if it doesn't exist yet
        couchDB = couchDBServer.database("leopardmon-testresults")
        logging.info("leopardmon-testresults DB successfully opened")

    except pycouchdb.exceptions.NotFound as e:
        couchDB = couchDBServer.create("leopardmon-testresults")
        logging.info("leopardmon-testresults does not exist - create the DB")

    # read the target information records

    targetInfos = testtarget.TargetInfoDict()
    targetInfos.loadFromDB()

    if (targetInfos.len == 0):
        targetInfo = createSampleTestTargets()
        targetInfo.store()


# *******************************************************************
# This is the main monitoring loop
# It is designed to run in a tread forever
# It loads the monitoring targets and parameters from the CouchDB
# and performs the monitoring operations.
# It sends e-mail on detected issues and writes all status to the CouchDB
# *******************************************************************

def monitoringLoop():

    # log start up message
    logging.info("***************************************************************")
    logging.info("LeopardMon monitoring thread has started")
    logging.info("Working directory is %s", os.getcwd())

    # create databases as needed
    createDBDocumentsIfNeeded()

    # now load all target entries
    targetInfos = testtarget.TargetInfoDict()
    targetInfos.loadFromDB()

    # build message body

    # loop through all targetinfo's and execute their tests
    monitoringBody = "The following properties are being monitored:\r\n"
    for key, target in targetInfos.targetInfos.items():
        assert isinstance(target.name, object)
        monitoringBody = monitoringBody + "\r\n" + target.name

    #mailhelper.sendMail("andreas.bauer@cellsignal.com", "Webproperty Monitor has started", monitoringBody)

    # run forever
    while (True):
        # loop through all targetinfo's and execute their tests
        for key, target in targetInfos.targetInfos.items():
            if (target.runCountdown < 1):
                target.executeTest()
                target.runCountdown = target.runInterval
            else:
                target.runCountdown = target.runCountdown - 1

        time.sleep(60)


