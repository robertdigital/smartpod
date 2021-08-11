import json
import uuid
import boto3
from botocore.exceptions import ClientError
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)

def generateUUID(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb')
    
    table = dynamodb.Table('seapod')
    uid = str(uuid.uuid4())
    isDuplicate = False

    
    try:
        response = table.scan()
        data = response['Items']

        while 'LastEvaluatedKey' in response:
            response = table.scan(ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])
    
    except ClientError as e:
        print(e.response['Error']['Message'])

    for item in data:
        pk = item['pk'];
        if pk == uid:
            logger.info("duplicate found, generating uuuid again")
            uid = generateUUID()
        logger.info("item info: %s",item['pk'])

    logger.info("UUID4 %s",uid)
    return uid;    

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
    logger.info("Request: %s", event)
    print("print ")
    response_code = 200
    
    http_method = event.get('httpMethod')
    query_string = event.get('queryStringParameters')
    headers = event.get('headers')
    body = event.get('body')
    
    logger.info("http_method: %s query_string: %s headers: %s body: %s",http_method,query_string,headers,body)
    logger.info(" generateUUID() == %s", generateUUID())
    seapodid = generateUUID()
    # event['id']
    name = event['name']
    port = event['port']
    
    logger.info("id: %s name: %s port: %s",seapodid,name,port)
    try:
        response = put_seapod(seapodid, name, port)
    except ClientError as e:
        print(e.response['Error']['Message'])
        logger.info

    response_code = response['ResponseMetadata']['HTTPStatusCode']
    responseMessage = 'Falied to add seapod'
    logger.info("response_code: %s",response_code)
    
    if response_code == 200:
        responseMessage = 'Successfully added seapod'
        
    logger.info("responseMessage: %s", responseMessage)
    
    response = {
        'statusCode': response_code,
        'body': json.dumps({'message': responseMessage, 'input': event})
    }    
    
    logger.info("Response: %s", response)
    return response
