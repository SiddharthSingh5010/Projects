import boto3
import botocore
import os

os.chdir('/home/ec2-user')

BUCKET_NAME = 'siddharthbucket501' # replace with your bucket name
KEY = 'Data_Final.csv' # replace with your object key
session = boto3.Session(
aws_access_key_id='#################',
aws_secret_access_key='#################'
)
s3 = session.resource('s3')
try:
    s3.Bucket(BUCKET_NAME).upload_file(KEY, 'Data_Final.csv')
except botocore.exceptions.ClientError as e:
    if e.response['Error']['Code'] == "404":
        print("The object does not exist.")
    else:
        raise