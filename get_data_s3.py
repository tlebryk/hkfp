import logging
import boto3
import pandas as pd
import re
import io
#%%
def read_s3(
    filedir,
    client=None,
    filepattern=None,
    bucket="hkfp",
    quiet=False,
    profile_name="default",
):
    """
    Reads in .csv files from S3 and returns a stacked dataframe
    Parameters
    ----------
    filedir : str
        File directory to search for CSV files
    client : str, optional
        S3 client (default is None, meaning S3 client is instantiated in function)
    filepattern : str, optional
        Pattern for files to read in; uses regex
        (default is None, meaning all .csv files are read in)
    bucket: str, optional
        Bucket to read data from (default is "protocol-china")
    """

    # instantiate S3 client if needed
    if client is None:
        botosession = boto3.Session(profile_name=profile_name)
        client = botosession.client("s3")
    # get everything in the bucket and directory
    # need to create paginator, otherwise limits to 1000 objects
    paginator = client.get_paginator("list_objects_v2")
    pages = paginator.paginate(Bucket=bucket, Prefix=filedir)

    is_match = True
    outlist = []
    for page in pages:
        for obj in page["Contents"]:
            key = obj.get("Key")
            # check for pattern matching if specified
            if filepattern is not None:
                matched = re.match(filepattern, key)
                is_match = bool(matched)
            # read in the CSV
            if is_match and ".csv" in key:
                if not quiet:
                    logging.info(f"Reading in {key} from S3")
                file_body = client.get_object(Bucket=bucket, Key=key).get("Body")
                df = pd.read_csv(io.BytesIO(file_body.read()))
                outlist.append(df)
            elif is_match and ".jl" in key:
                if not quiet:
                    logging.info(f"Reading in {key} from S3")
                file_body = client.get_object(Bucket=bucket, Key=key).get("Body")
                df = pd.read_json(io.BytesIO(file_body.read()), lines=True)
                outlist.append(df)
    # return stacked dataframe
    return pd.concat(outlist)



def read_single_csv(bucket, file_name):
    s3 = boto3.client('s3') 
    # 's3' is a key word. create connection to S3 using default config and all buckets within S3

    obj = s3.get_object(Bucket= bucket, Key= file_name) 
    # get object and file (key) from bucket

    initial_df = pd.read_csv(obj['Body']) # 'Body' is a key word

if __name__ == "__main__":
    pass
# %%
df = read_single_csv('hkfp', 'data/allscrape_20211129_172540.csv')

df = read_s3('data', profile_name='default')