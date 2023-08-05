import logging
import boto3
logger = logging.getLogger(__name__)


def get_object_from_s3(bucket_name: str, object_key: str, s3_client: boto3.Session.client):
    logger.info(f"Downloading object: s3://{bucket_name}/{object_key}")
    response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
    content = response['Body'].read().decode('utf-8')
    return content


def write_simple_object_to_s3(content: str, bucket_name: str, object_key: str, s3_client: boto3.Session.client):
    """Write an object to S3 with basic AES256 encryption"""
    logger.info(f"Writing object: s3://{bucket_name}/{object_key}")
    response = s3_client.put_object(
        ACL="private",
        Bucket=bucket_name,
        Key=object_key,
        ServerSideEncryption="AES256",
        Body=content
    )
    logger.debug(response)
