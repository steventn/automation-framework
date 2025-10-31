import boto3
from botocore.exceptions import ClientError


# Simple S3 Service Class
class SimpleS3Service:
    def __init__(self):
        self.s3_client = boto3.client('s3', region_name='us-east-1')

    def create_bucket(self, bucket_name):
        try:
            self.s3_client.create_bucket(Bucket=bucket_name)
            return True
        except ClientError:
            return False

    def upload_file(self, bucket_name, file_name, content):
        try:
            self.s3_client.put_object(
                Bucket=bucket_name,
                Key=file_name,
                Body=content
            )
            return True
        except ClientError:
            return False

    def download_file(self, bucket_name, file_name):
        try:
            response = self.s3_client.get_object(
                Bucket=bucket_name,
                Key=file_name
            )
            return response['Body'].read().decode('utf-8')
        except ClientError as e:
            print(e)
            return None

    def list_buckets(self):
        try:
            response = self.s3_client.list_buckets()
            return [bucket['Name'] for bucket in response['Buckets']]
        except ClientError:
            return []

    def delete_bucket(self, bucket_name):
        try:
            # Delete all objects first
            objects = self.s3_client.list_objects_v2(Bucket=bucket_name)
            if 'Contents' in objects:
                for obj in objects['Contents']:
                    self.s3_client.delete_object(Bucket=bucket_name, Key=obj['Key'])

            # Then delete bucket
            self.s3_client.delete_bucket(Bucket=bucket_name)
            return True
        except ClientError:
            return False