
import base64
import json
import os
import time, random


pause = os.environ['PAUSE']
def lambda_handler(event, context):
    '''
    Sink records from Kinesis and optionally sleep for PAUSE + a random between [-0.5,0.5) seconds 
    '''
    print('Successfully sinked {} records.'.format(len(event['Records'])))
    if pause and float(pause)>0.5:
        sleeptime = int(1000 * (float(pause) - 0.5 + random.random())) /1000.0
        print ("Sleeping {} seconds".format(sleeptime))
        time.sleep(sleeptime)  
