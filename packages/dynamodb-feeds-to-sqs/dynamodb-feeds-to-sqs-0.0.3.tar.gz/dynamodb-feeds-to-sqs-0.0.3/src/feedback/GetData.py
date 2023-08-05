import boto3
import logging
import os

from boto3.dynamodb.conditions import Key
from dotenv import load_dotenv

''' Loading Environment files '''
load_dotenv()


class GetData:
    def __init__(self, region, table, columnToCheck):
        self.region = region
        self.table = table
        self.columnToCheck = columnToCheck

    def scanTable(self):
        dynamoDbResource = boto3.resource(os.getenv("AWS_DYNAMO"), region_name=self.region)
        tableResource = dynamoDbResource.Table(self.table)
        try:
            allRecords = tableResource.scan()
            updatedRecords =[]
            print(allRecords)
            for record in allRecords['Items']:
                if record['isTrue']=="true":
                    updatedRecords.append(record)
                    tableResource.update_item(
                        Key={'hash': record['hash']},
                        UpdateExpression="set "+self.columnToCheck+" = :it",
                        ExpressionAttributeValues={
                            ':it': 'false',
                        },
                        ReturnValues="UPDATED_NEW"
                    )
        except Exception as e:
            print(e)
        return updatedRecords
