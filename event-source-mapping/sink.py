
import base64
import json



def lambda_handler(event, context):
    print('Successfully sinked {} records.'.format(len(event['Records'])))
