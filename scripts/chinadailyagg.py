# %%
import pandas as pd
import os

dir = r"C:\Users\tlebr\OneDrive - pku.edu.cn\Thesis\data\chinadaily"
df = pd.concat(
    pd.read_json(os.path.join(dir, f), lines=True) for f in os.listdir(dir)
)

# %%
df.columns
# %%
drop_cols = [
    "inner_id",
    "tags",  # keywords is better
    "created",  # check if this sucks
    "content",
    "system",
    "author_low",
    "type",
    "originalId",
    "channelId",
    "img",
    "dupTitle",
    "categories",
    "thumbnailStyle",
    "contentType",
    "canComment",
    "wordCount",
    "imageCount",
    "leadinLine",
    "images",
    "thumbnails",
    "columnDirname",
    "mediaStream",
    "resources",
    "properties", # save separately?
    "comment",
    "originUri",
    "expired",  # check
    "specialId",
    "editorRecommends", # save separately
    "originSpecialId",
    "columnId",
    "highlight",
    "highlightTitle",
    "highlightContent",
]
dropped = df.drop(drop_cols, axis=1)
dropped.to_csv(r"C:\Users\tlebr\OneDrive - pku.edu.cn\Thesis\data\chinadaily\cd_full.csv")
# %%
import boto3
def upload_s3(filepath, bucket, key=None):
    if not key:
        key = filepath
    try:
        response = s3_client.upload_file(filepath, bucket, key)
        return response
    except ClientError as e:
        logging.exception(e)
upload_s3(
    r"C:\Users\tlebr\OneDrive - pku.edu.cn\Thesis\data\chinadaily\cd_full.csv", 
    bucket="newyorktime",
    "chinadaily/chinadaily_full.csv"
    )

dropped
# %%
df.properties.iloc[0]
.explode().value_counts()
df.highlightTitle.value_counts()
df.head()
