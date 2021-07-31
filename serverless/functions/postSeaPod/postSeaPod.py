import json
import boto3
from botocore.exceptions import ClientError


def put_seapod(seapodid, name, port, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('seapod')
    response = table.put_item(
       Item={
            'pk': seapodid,
            'sk': name,
            'port': port
        }
    )
    return response


def lambda_handler(event, context):
    seapodid = event['id']
    name = event['name']
    port = event['port']

    try:
        response = put_seapod(seapodid, name, port)
    except ClientError as e:
        print(e.response['Error']['Message'])

    responseCode = response['ResponseMetadata']['HTTPStatusCode']
    responseMessage = 'Falied to add seapod'
    if responseCode == 200:
        responseMessage = 'Successfully added seapod'
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(responseMessage)
    }
