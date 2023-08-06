#!/usr/bin/env python3
# Python Library Imports
import logging
import boto3
from botocore.exceptions import ClientError, NoCredentialsError, BotoCoreError


def upload_file(bucket, key, filename, encryption=None):
    logging.info(f"Uploading File {filename} to {key}")
    try:
        if encryption:
            bucket.upload_file(
                filename, key, ExtraArgs={"ServerSideEncryption": encryption}
            )
        else:
            bucket.upload_file(filename, key)
    except Exception as err:
        logging.exception(f"Exception uploading file: {err}")
        raise

