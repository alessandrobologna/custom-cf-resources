import boto3
import os
import datetime
import uuid
import json
import time

kinesis_client = boto3.client('kinesis')

stream = os.environ['EVENT_STREAM']

def lambda_handler(event, context):
    '''
    Sample loader with 6000 records/minute througput
    '''

    while True:
        response = kinesis_client.put_record(
            StreamName=stream,
            Data=datetime.datetime.now().isoformat(),
            PartitionKey=str(uuid.uuid4())
        )
        print("Sent record: \n" + json.dumps(response))
        time.sleep(0.01)

