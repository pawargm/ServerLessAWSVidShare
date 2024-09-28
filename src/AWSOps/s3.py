import json
import boto3
import logging
from botocore.exceptions import ClientError
logger = logging.getLogger(__name__)


class S3:

    '''
    Constructor for creating S3
    '''
    def __init__(self, region, bucketName):

        self.region = region
        self.bucketName = bucketName
        
        #creating instance for s3 
        self.s3Client = boto3.client('s3')
    

    '''
    Get presigned URL for S3 upload
    '''
    def getPreSignedUploadUrl(self, key, expiresIn):
        
        print("getPreSignedUploadUrl")
        print(self.bucketName)
        print(key)
        print(expiresIn)

        presigned_url = self.s3Client.generate_presigned_url('put_object', 
                                                    Params={
                                                        'Bucket': self.bucketName,
                                                        'Key': key
                                                    },
                                                    ExpiresIn= expiresIn,
                                                    HttpMethod = "put"
                                                    )
        return presigned_url

    '''
    Get presigned URL for S3 download
    '''
    def getPreSignedDownloadUrl(self, key, expiresIn):

        presigned_url = self.s3Client.generate_presigned_url('get_object', 
                                                    Params={
                                                        'Bucket': self.bucketName,
                                                        'Key': key
                                                    },
                                                    ExpiresIn= expiresIn,
                                                    HttpMethod = "get"
                                                    )
        return presigned_url


    '''
    To delete s3 object
    '''
    def deleteObject(self, key):
        print("deleteObject")
        response = self.s3Client.delete_object(Bucket=self.bucketName, Key=key)
        print(response)
        return response
        