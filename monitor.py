#!/usr/bin/python3.6

import logging
from mailhelper import mailhelper
from monitor import leopardmon
import threading


def main():
    # set up the logger
    logging.basicConfig(filename = "leopardmon.log", format='%(asctime)s %(levelname)s %(message)s',
                        level=logging.INFO)

    mailhelper.readUsernamePassword()

    # start the monitoring loop
    monitoringThread = threading.Thread(target = leopardmon.monitoringLoop())
    monitoringThread.start()

    while (true):
        time.sleep(60)

main()