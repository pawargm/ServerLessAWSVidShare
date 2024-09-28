import json
import boto3
import logging
from botocore.exceptions import ClientError
logger = logging.getLogger(__name__)


class DB:

    '''
    Constructor with tableName, region  
    '''
    def __init__(self, region, tableName):
        self.tableName = tableName
        self.region = region

        #creating instance for s3 
        self.dynamoDBClient = boto3.client('dynamodb')

    '''
    Function to get data from dynamoDB id.
    '''
    def get(self, id):
        
        getItem = self.dynamoDBClient.get_item(
            TableName=self.tableName,
            key = {
                "id": {'S': id}
            }
        )

        return getItem

    '''
    Function to put data to dynamoDB with docItem
    '''
    def put(self, dynamoDBDict):
        #Below code for event notification code changes extract 
        id = dynamoDBDict['bucketName'] + dynamoDBDict['fileName']

        PutItem = self.dynamoDBClient.put_item(
            TableName=self.tableName,
            Item = {
                "id": {'S': id},
                "bucketName": {'S': dynamoDBDict['bucketName'] },
                "fileName": {'S': dynamoDBDict['fileName'] },
                "fileSizeInByte": {'N': str(dynamoDBDict['fileSize']) }
                
            }
        )
    
    '''
    Function to update to dynamoDB
    '''
    def update(self, id, attrs):
        pass



'''
#Skeleton code for handler to handle business logic

import json

def lambda_handler(event, context):
    """Handles incoming events and dispatches them to appropriate business logic functions.

    Args:
        event (dict): The event data received by the Lambda function.
        context (LambdaContext): The Lambda context object.

    Returns:
        dict: The response to be returned by the Lambda function.
    """

    # Parse the event data to extract the event type
    event_type = event.get("type")

    # now here using type but for internal aws call got from event bridge it 
    # should do deligate call based on source or request id

    #example might be these field get in event 

    {
    
        {
            "version": "0",
            "id": "17793124-05d4-b198-2fde-7ededc63b103",
            "detail-type": "Object Created",
            "source": "aws.s3",
            "account": "123456789012",
            "time": "2021-11-12T00:00:00Z",
            "region": "ca-central-1",
            "resources": ["arn:aws:s3:::example-bucket"],
            "detail": {
                "version": "0",
                "bucket": {
                "name": "example-bucket"
                },
                "object": {
                "key": "example-key",
                "size": 5,
                "etag": "b1946ac92492d2347c6235b4d2611184",
                "version-id": "IYV3p45BT0ac8hjHg1houSdS1a.Mro8e",
                "sequencer": "00617F08299329D189"
                },
                "request-id": "N4N7GDK58NMKJ12R",
                "requester": "123456789012",
                "source-ip-address": "1.2.3.4",
                "reason": "PutObject"
            }
        }
    } 


    # Define a dictionary mapping event types to corresponding handler functions
    handlers = {
        "create_order": create_order,
        "update_order": update_order,
        "delete_order": delete_order,
    }

    # Dispatch the event to the appropriate handler function
    if event_type in handlers:
        handler = handlers[event_type]
        response = handler(event)
    else:
        # Handle unsupported event type
        response = {
            "statusCode": 400,
            "body": json.dumps({"message": "Unsupported event type"})
        }

    return response

def create_order(event):
    # Implementation for creating an order
    # ...
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Order created successfully"})
    }

def update_order(event):
    # Implementation for updating an order
    # ...
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Order updated successfully"})
    }

def delete_order(event):
    # Implementation for deleting an order
    # ...
    return {
        "statusCode": 200,
        "body": json.dumps({"message": "Order deleted successfully"})
    }

#backup from AWS
#vidshare-puthandler

import json
import boto3
import logging
from botocore.exceptions import ClientError
logger = logging.getLogger(__name__)

def lambda_handler(event, context):
    # TODO implement
    response = {}
    presigned_url = ""
    try:
        
        print("presigned_url-V2")
        s3 = boto3.client('s3')
        file_to_upload = event['body']
    
        bucket_name = "test-goppaw07-1"
        bucket_key = "test-goppaw07-pdf4-key"
    
        response = s3.put_object(
                    Bucket=bucket_name,
                    Key=bucket_key,
                    Body=file_to_upload
                    )
        
        presigned_url = s3.generate_presigned_url('put_object', Params={'Bucket': 'test-goppaw07-1',
                                                                                'Key': 'my_upload2'
                                                                              },ExpiresIn=600, HttpMethod="put")
        
        # Build the redirect response
        response = {
            'statusCode': 302,  # HTTP status code for PUT redirect
            'body': json.dumps(presigned_url)
        }
        print("Inside")
        print(presigned_url)
        print("-----")
        return response
    except ClientError as err:
        logger.error(
            "Couldn't add movieto table Test. Here's why: %s: %s",
            err.response["Error"]["Code"],
            err.response["Error"]["Message"],
        )
    return response
    
    
    table = boto3.client('dynamodb')
    PutItem = None;
    body_str = event['body']
    body_str = body_str if body_str else "{}"
    body_obj = json.loads(body_str)
    print("ttt")
    print(body_obj.get("name", ""))
    
    try:
        PutItem = table.put_item(
            TableName='Test',
            Item = {
                "name": {'S':body_obj.get("name", "")},
                "age": {'S':body_obj.get("age", "")}
                
            }
        )
    except ClientError as err:
        logger.error(
            "Couldn't add movieto table Test. Here's why: %s: %s",
            err.response["Error"]["Code"],
            err.response["Error"]["Message"],
        )
    return {
        'statusCode': 200,
        'body': json.dumps(PutItem)
    }
    
    
    #S3EventHandler

    import json

import boto3
import logging
from botocore.exceptions import ClientError
logger = logging.getLogger(__name__)


def lambda_handler(event, context):
    # TODO implement
    print(event)
    
    
    #Below code for event notification code changes extract 
    evenObject = event['Records'][0]
   
    print(type(evenObject))
    bucketName = evenObject['s3']['bucket']['name']
    fileName = evenObject['s3']['object']['key']
    fileSize = evenObject['s3']['object']['size']
    
    
    evenObject = event['detail']
   
    print(type(evenObject))
    bucketName = evenObject['bucket']['name']
    fileName = evenObject['object']['key']
    fileSize = evenObject['object']['size']

    table = boto3.client('dynamodb')
    
    try:
        PutItem = table.put_item(
            TableName='vidshare-video',
            Item = {
                "id": {'S': "Test"},
                "bucketName": {'S': bucketName },
                "fileNameOrKey": {'S': fileName },
                "fileSizeInByte": {'N': str(fileSize) }
                
            }
        )
    except ClientError as err:
        logger.error(
            "Couldn't add movieto table Test. Here's why: %s: %s",
            err.response["Error"]["Code"],
            err.response["Error"]["Message"],
        )
    
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }

'''
    



    
