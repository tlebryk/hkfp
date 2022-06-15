"""Pass a year (e.g. 2013) and will upload that json
lines file to s3. """
import sys
import logging

import boto3
from botocore.exceptions import ClientError

s3_client = boto3.client("s3")

def upload_s3(filepath, bucket, key=None):
    if not key:
        key = filepath
    try:
        response = s3_client.upload_file(filepath, bucket, key)
        return response
    except ClientError as e:
        logging.exception(e)

if __name__ == "__main__":
    print(sys.argv[1])
    bucket="newyorktime"
    # 2 char year such as 2012->12
    yr = sys.argv[1][-2:]
    filepath = f"cdaily{yr}.jl"
    key=f"chinadaily/{yr}/{filepath}"
    response = upload_s3(filepath, bucket, key)
    print(response)


    