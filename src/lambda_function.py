import json
import boto3
import logging
from AWSOps import s3
from AWSOps import s3EventToDynamoDB
from botocore.exceptions import ClientError
logger = logging.getLogger(__name__)


#to do action
#since it is global so we need to protect it from race condition
s3Dict = {}

#to do action
#since it is global so we need to protect it from race condition
dynamoDBDict = {}

def lambda_handler(event, context):

    response = None
    print("context")
    print(context.function_name)
    print(event)
    source = event['source'] if "source" in event else ""
    print("Source ")
    print(source)
    try:
        if source == "aws.s3":
            #It means that event should update event data to dynamodb 
            extractDeatilsForDynamoDB(event)
            s3EventToDynamoDB1 = s3EventToDynamoDB.DB("mumbai", "videoMetaData")
            updateEventToDynamoDB(s3EventToDynamoDB1)
        else:
            # Parse the event data to extract the event type
            extractS3DeatilsFromReq(event)
            s3Object = s3.S3("mumbai", s3Dict['bucketName'])
            response = actionsFromClient(event, s3Object)

    except ClientError as err:
        logger.error(
            "Couldn't add movieto table Test. Here's why: %s: %s",
            err.response["Error"]["Code"],
            err.response["Error"]["Message"],
        )
    
    if response != None:
        return response

    return {
        'statusCode': 200,
        'body': json.dumps('Ok from Lambda!')
    }



#function to update event from AWS event bridge
def updateEventToDynamoDB(s3EventToDynamoDB1):
    s3EventToDynamoDB1.put(dynamoDBDict)


#Util function to extract s3 data from event body
def extractDeatilsForDynamoDB(event):
    global dynamoDBDict
    evenObject = event['detail']
    dynamoDBDict['bucketName'] = evenObject['bucket']['name']
    dynamoDBDict['fileName'] = evenObject['object']['key']
    dynamoDBDict['fileSize'] = evenObject['object']['size']
    
#Util function to extract s3 data from event body
def extractS3DeatilsFromReq(event):
    global s3Dict
    reqBodyStr = event['body']

    reqBodyStr = reqBodyStr if reqBodyStr else "{}"
    reqBodyObj = json.loads(reqBodyStr)
    bucketName = reqBodyObj.get("bucketName", "")
    s3Key = reqBodyObj.get("key", "")
    s3Dict['bucketName'] = bucketName
    s3Dict['key'] = s3Key
    s3Dict['type'] = reqBodyObj.get("type", "")

#function to take care of client request to AWS lambda
def actionsFromClient(event, s3Object):

    event_type = s3Dict['type']
    presigned_url = ""
    
    print("EventType")
    print(event_type)
    
    if event_type == "getPreSignedUploadUrl":
        #Call getPreSignedUploadUrl
        #hardcoding expiring time for 5 mins
        presigned_url = s3Object.getPreSignedUploadUrl(s3Dict['key'], 300)

    elif event_type == "getPreSignedDownloadUrl":
        #Call getPreSigneddownloadURL
        presigned_url = s3Object.getPreSignedDownloadUrl(s3Dict['key'], 300);

    elif event_type == "deleteSomeObject":
        #Call deleteObject
        response = s3Object.deleteObject(s3Dict['key'])
        resp = None
        if response['HTTPStatusCode'] == 204:
            resp = {
                'statusCode': 200,
                'body': json.dumps('Ok from Lambda!')
                }
        return resp
    else:
        pass

    # Build the redirect response
    response = {
        'statusCode': 302,  # HTTP status code for PUT redirect
        'body': json.dumps(presigned_url)
    }

    return response
