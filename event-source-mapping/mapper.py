import json
import boto3
from botocore.vendored import requests
import json
from datetime import datetime
import time, random

SUCCESS = "SUCCESS"
FAILED = "FAILED"


json.JSONEncoder.default = lambda self,obj: (obj.isoformat() if isinstance(obj, datetime) else None)

def send(event, context, status, data, physicalResourceId, reason=None):
    '''
    Update CloudFormation with the Custom Resource progress
    '''
    url = event['ResponseURL']
    body = {
        'Status' : status,
        'Reason' : reason,
        'PhysicalResourceId' : physicalResourceId,
        'LogicalResourceId' : event['LogicalResourceId'],
        'StackId' : event['StackId'],
        'RequestId' : event['RequestId'],
        'Data' : data
    }
    json_body = json.dumps(body)
    headers = {'content-type': '', 'content-length': str(len(json_body))}
    try:
        response = requests.put(url, data=json_body, headers=headers)
        print("Status code: " + response.reason)
    except Exception as e:
        print("Failed updating CloudFormation: " + str(e))
    return None


def lambda_handler(event, context):
    try:
        data = {}
        reason = ""
        print("Received event: \n" + json.dumps(event))
        # determine current region and create client
        region = event['ServiceToken'].split(':')[3]
        client = boto3.client('lambda', region)

        mapping = event['ResourceProperties']
        if mapping:
            mapping.pop("ServiceToken")
            mapping['BatchSize'] = int(mapping.get('BatchSize', '100'))
            mapping['Enabled'] = mapping.get('Enabled', 'True').lower() in ('yes', 'true', 'sure', 'yup')

            attempt = 0
            # get out of the loop if remaining time is less than 5 seconds
            while context.get_remaining_time_in_millis() > 5000:
                print ("entering loop")
                try:
                    # create mapping
                    if event['RequestType'] == "Create":
                        print("Creating Mapping: \n" + json.dumps(mapping))
                        response = client.create_event_source_mapping(**mapping)
                        print("Response: \n" + json.dumps(response))
                        data['UUID'] = response['UUID']
                        return send(event, context, SUCCESS, data, response['UUID'], "Success")
                    else:
                        if event.get('PhysicalResourceId'):
                            if event['RequestType'] == "Delete":
                                try:
                                    response = client.delete_event_source_mapping(
                                        UUID = event.get('PhysicalResourceId')
                                    )
                                    print("Delete response: \n" + json.dumps(response))
                                except Exception as e:
                                    # avoid error state if resource was not found
                                    if not 'ResourceNotFoundException' in str(e):
                                        raise e
                                    print ("Error during delete, will still return success: " + str(e))
                                return send(event, context, SUCCESS, data, response['UUID'], "Deleted")
                            if event['RequestType'] == "Update":
                                print("Updating Mapping: \n" + json.dumps(mapping))
                                response = client.update_event_source_mapping(
                                    UUID = event.get('PhysicalResourceId'),
                                    FunctionName = mapping.get('FunctionName'),
                                    Enabled = mapping.get('Enabled'),
                                    BatchSize = mapping.get('BatchSize')
                                )
                                print("Update response: \n" + json.dumps(response))
                                return send(event, context, SUCCESS, data, response['UUID'], "Updated")
                        else:
                            # looks like bad CF code
                            reason = "Missing PhysicalResourceId"
                            return send(event, context, FAILED, data, None, reason)
                except Exception as e:
                    # retry for retriable exceptions
                    if not any (exception in str(e) for exception in ('LimitExceededException','ProvisionedThroughputExceededException')):
                        raise e
                    sleeptime = 1 + random.random()
                    attempt = attempt + 1
                    print ("Attempt {} caused {}, retrying after {} seconds".format(str(attempt), str(e), sleeptime))
                    time.sleep(sleeptime)  
                    print ("retrying loop")
                    continue
            # exiting the loop. we have timed out
            reason = "Timeout during " + event['RequestType']
        else:
            reason = "Missing Mapping information"
    except Exception as e:
        reason = str(e)
    
    print(reason)
    send(event, context, FAILED, data, event.get('PhysicalResourceId'), reason)
    return
