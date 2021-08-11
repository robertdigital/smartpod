import json
import uuid
import boto3
from botocore.exceptions import ClientError
from boto3.dynamodb.types import TypeDeserializer
import logging


logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler_core(event, context):
    try:
        logger.info("Request: %s", event)
        print("print ")
        response_code = 200

        http_method = event.get('httpMethod')
        query_string = event.get('queryStringParameters')
        headers = event.get('headers')
        body = event.get('body')

        logger.info("http_method: %s query_string: %s headers: %s body: %s",
                    http_method, query_string, headers, body)

        logger.info(" generateUUID() == %s", generateUUID())
        seapodid = generateUUID()
        name = event['name']
        port = event['port']

        logger.info("id: %s name: %s port: %s", seapodid, name, port)
        try:
            response = put_seapod(seapodid, name, port)
        except ClientError as e:
            print(e.response['Error']['Message'])
            logger.error("Error %s", e.response['Error'])
            raiseException(e)

        response_code = response['ResponseMetadata']['HTTPStatusCode']
        responseMessage = 'Falied to add seapod'
        logger.info("response_code: %s", response_code)

        if response_code == 200:
            responseMessage = 'Successfully added seapod'

        logger.info("responseMessage: %s", responseMessage)

        response = {
            "statusCode": response_code,
            "isError": False,
            "type": "na",
            "message": responseMessage
        }

        logger.info("Response: %s", response)
        return response

    except ClientError as e:
        logger.error("Client error code %s", e.response['Error']['Code'])
        raiseException(e)


def raiseException(e):

    if e.response['Error']['Code'] == "404":
        raise ClientException("Not Found")
    elif e.response['Error']['Code'] == "403":
        raise ClientException("Forbidden")
    elif e.response['Error']['Code'] == "400":
        raise ClientException("Bad Request")
    elif e.response['Error']['Code'] == "500":
        raise ClientException("Internal Server Error")
    else:
        raise ClientException("Undefined exception")


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
            response = table.scan(
                ExclusiveStartKey=response['LastEvaluatedKey'])
            data.extend(response['Items'])

    except ClientError as e:
        print(e.response['Error']['Message'])

    for item in data:
        pk = item['pk']
        if pk == uid:
            logger.info("duplicate found, generating uuuid again")
            uid = generateUUID()
        logger.info("item info: %s", item['pk'])

    logger.info("UUID4 %s", uid)
    return uid


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


def ddb_deserialize(r, type_deserializer=TypeDeserializer()):
    return type_deserializer.deserialize({"S": r})


def lambda_handler(event, context):
    try:
        response = ddb_deserialize(handler_core(event, context))
        return response
    except Exception as e:
        exception_type = e.__class__.__name__
        exception_message = str(e)

        api_exception_obj = {
            "statusCode": 400,
            "isError": True,
            "type": exception_type,
            "message": exception_message
        }

        # Create a JSON string
        api_exception_json = json.dumps(api_exception_obj)
        logger.error("Error %s", str(api_exception_json))
        return api_exception_obj
        # raise ClientException(api_exception_json)
