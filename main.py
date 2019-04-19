#!/usr/bin/python3.6

# logging facility: https://realpython.com/python-logging/
import logging
import os

from target import testtarget


def main():

    # set up the logger
    logging.basicConfig(filename = "leopardmon.log", format='%(asctime)s %(levelname)s %(message)s',
                        level=logging.INFO)

    # log start up message
    logging.info("***************************************************************")
    logging.info("LeopardMon has started")
    logging.info("Working directory is %s", os.getcwd())

    code = """
print('Hello Japan')
    """


    targetInfo = testtarget.TargetInfo("Japan Inventory and Pricing Microservice",
                code, "Executing test code for: %s", self.name)
    targetInfo.executeTest()

main()