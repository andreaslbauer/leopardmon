import pycouchdb
import logging

def dbCreateIfNeeded():
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

    try:
        # create the couchdb instance - if it doesn't exist yet
        couchDB = couchDBServer.database("leopardmon-users")
        logging.info("leopardmon-users DB successfully opened")

    except pycouchdb.exceptions.NotFound as e:
        couchDB = couchDBServer.create("leopardmon-users")
        logging.info("leopardmon-users does not exist - create the DB")


def dbPutUser(name, password):
    couchDBServer = pycouchdb.Server()
    couchDB = couchDBServer.database("leopardmon-users")

    doc = {}
    doc["_id"] = name
    doc["name"] = name
    doc["password"] = password

    couchDB.save(doc)

def dbGetUser(name):
    couchDBServer = pycouchdb.Server()
    couchDB = couchDBServer.database("leopardmon-users")
    doc = None
    try:
        doc = couchDB.get(name)
    except pycouchdb.exceptions.NotFound as e:
        doc = None

    return doc
