# one off script to upload csvs to s3 bucket
import boto3
import pandas as pd
s3_client = boto3.client("s3")

# %%
# deduplicate commenters:
df = pd.read_csv("data/globaltimes/CommenterItem/20211228_154428.csv")
df = df.drop_duplicates()
df.to_csv("data/globaltimes/CommenterItem/20211228_154428 (2).csv")
# %%
response = s3_client.upload_file("data/globaltimes/ArticleItem/20211228_154428.csv", "globaltimes", "data/articles/20211228_154428.csv")
response = s3_client.upload_file("data/globaltimes/CommenterItem/20211228_154428 (2).csv", "globaltimes", "data/commenters/20211228_154428.csv")
response = s3_client.upload_file("data/globaltimes/CommentItem/20211228_154428.csv", "globaltimes", "data/comments/20211228_154428.csv")

