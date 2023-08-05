import json
import schedule
import time
import boto3
import os

from dotenv import load_dotenv

from src import GetData

''' Loading Environment files '''
load_dotenv()

class Scheduler:
    def __init__(self, columns, isAllColumn, feedScheduler, table, tableRegion, queueName, queueRegion,
                 isStartScheduler, columnToCheck):
        self.columns = columns
        self.isAllColumn = isAllColumn
        self.feedScheduler = feedScheduler
        self.table = table
        self.queueName = queueName
        self.isStartScheduler = isStartScheduler
        self.tableRegion = tableRegion
        self.queueRegion = queueRegion
        self.columnToCheck = columnToCheck

    def schedulerJob(self):
        sqs_client = boto3.client(os.getenv("AWS_SQS"), region_name=self.queueRegion)
        getData = GetData(self.tableRegion, self.table, self.columnToCheck)
        dbData=getData.scanTable()
        if(len(dbData) >0):
            if(self.isAllColumn):
                print("Set all Columns")
                queueResponse = sqs_client.get_queue_url(QueueName=self.queueName)
                queue_url = queueResponse['QueueUrl']
                response = sqs_client.send_message(QueueUrl=queue_url, MessageBody=json.dumps(dbData))
                print("queue response {}".format(response))

            else:
                print("Set selected Columns {}".format(self.columns))

    def scheduler(self):
        print("Started Scheduling ...")
        schedule.every(self.feedScheduler).seconds.do(self.schedulerJob)

        while self.isStartScheduler:
            schedule.run_pending()
            time.sleep(self.feedScheduler/10)

    def stop(self):
        self.isStartScheduler=False