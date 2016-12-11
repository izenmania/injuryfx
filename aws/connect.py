from credentials import load
import boto3

conf = load.conf


def open():
    """Opens an s3 client using the site's stored AWS credentials"""
    return boto3.client(
        's3',
        aws_access_key_id = conf['aws']['key'],
        aws_secret_access_key = conf['aws']['secret']
    )
