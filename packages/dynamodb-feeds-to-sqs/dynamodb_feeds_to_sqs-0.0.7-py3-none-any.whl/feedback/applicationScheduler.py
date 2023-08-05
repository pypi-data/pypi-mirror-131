import logging
import time

from feedback import Scheduler
from threading import Thread

class DataFormation:
    def __init__(self, tableRegion, table, columns, isAllColumn, feedScheduler,queueName, queueRegion,columnToCheck):
        self.tableRegion = tableRegion
        self.table = table
        self.columns = columns
        self.isAllColumn = isAllColumn
        self.feedScheduler = feedScheduler
        self.queueName = queueName
        self.queueRegion = queueRegion
        self.isStartScheduler = True
        self.columnToCheck = columnToCheck

    def initialization(self):
        logging.info("Initialized tableRegion "+self.tableRegion)
        logging.info("Initialized table "+self.table)
        logging.info("Initialized columns {}".format(self.columns))
        logging.info("Initialized isAllColumn {}".format(self.isAllColumn))
        logging.info("Initialized feedScheduler {}".format(self.feedScheduler))
        logging.info("Initialized queueRegion ".format(self.queueRegion))

    def schedulerStop(self):
        logging.info("Stopping Scheduler...")
        print("Stopping Scheduler...")
        schedulerResponse.stop()

    def schedulerStart(self, time):
        logging.info("Starting Scheduler...")
        self.isStartScheduler = True
        logging.info("Scheduler time ".format(time))
        global schedulerResponse
        schedulerResponse = Scheduler.Scheduler(self.columns, self.isAllColumn, self.feedScheduler, self.table,
                                                self.tableRegion, self.queueName, self.queueRegion,
                                                self.isStartScheduler, self.columnToCheck)
        t = Thread(target=schedulerResponse.scheduler)
        t.start()

# data = DataFormation('us-east-1','test2',[],True,10,'student_trade_app_feed_queue','us-east-1','isTrue')
#
# data.initialization()
#
# data.schedulerStart(3)
#
# time.sleep(30)
# data.schedulerStop()