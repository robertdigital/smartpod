import json
import boto3
from botocore.exceptions import ClientError
import os


def getAllSeaPods(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')
        
    table = dynamodb.Table('seapod')
    
    try:
        response = table.scan()
        data = response['Items']

        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        return data
        
       
def lambda_handler(event, context):
    print('invoking get all seapods')
    seapods = getAllSeaPods()
    print(seapods)
    return {
        'statusCode': 200,
        'body': json.dumps(seapods)
    }