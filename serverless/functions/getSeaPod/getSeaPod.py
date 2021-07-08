# import json

# def lambda_handler(event, context):
#     # TODO implement
#     return {
#         'statusCode': 200,
#         'body': json.dumps('Hello from Lambda!')
#     }

import json
import boto3
from botocore.exceptions import ClientError
import os


def getAllSeaPods(dynamodb=None):
    if not dynamodb:
        # dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")
        dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('seapod')
    
    try:
        # response = table.scan(**scan_kwargs)
        response = table.scan()
        # response = table.get_item()
        data = response['Items']

        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        # return response['Item']
        return data
        
# def lambda_handler(event, context):        
#     print(event.routeKey)
#     json_region = os.environ['AWS_REGION']
#     return {
#         "statusCode": 200,
#         "headers": {
#             "Content-Type": "application/json"
#         },
#         "body": json.dumps({
#             "Region ": json_region
#         })
#     }        
def lambda_handler(event, context):
    # TODO implement
    print('invoking get all seapods')
    seapods = getAllSeaPods()
    print(seapods)
    return {
        'statusCode': 200,
        'body': json.dumps(seapods)
    }
