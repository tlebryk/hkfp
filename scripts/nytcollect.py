import newspaper
from time import sleep
from newspaper.article import ArticleException, ArticleDownloadState
import pandas as pd
import boto3
import logging

logging.basicConfig(filename="scrape.log", level=logging.info)
logger = logging.getLogger(__name__)

# from newsplease import NewsPlease

# Parse article
# s3 = boto3.client("s3")
# s3.download_file("newyorktime", "nyt/clean_main.csv", "clean_main.csv")

# df  =pd.read_csv("clean_main.csv")

#  pd.read_csv(r"C:\Users\tlebr\OneDrive - pku.edu.cn\Thesis\data\nyt\clean_main.csv")


def scrape(url):
    # Download article
    slept = 0
    article = newspaper.Article(url=url)
    article.download()
    while article.download_state == ArticleDownloadState.NOT_STARTED:
        # Raise exception if article download state does not change after 10 seconds
        if slept > 9:
            raise ArticleException("Download never started")
        sleep(1)
        slept += 1
    article.parse()
    obj = {
        "title": article.title,
        "authors": article.authors,
        "text": article.text,
        "keywords": article.keywords,
        "tags": article.tags,
        # article.source_url,
        "newurl": article.url,
        "sourceurl": url,
    }
    return obj


urls = df.head().web_url.tolist()
badurls = []
objs = []
for url in urls:
    try:
        obj = scrape(url)
        if obj:
            objs.append(obj)
    except Exception as e:
        logger.error(e)
        badurls.append(url)

maindf = pd.json_normalize(objs)  # .maintext.iloc[0]
maindf.to_csv("nyt_full.csv")

with open("badfiles.txt", "a") as f:
    for u in badurls:
        f.write(u)

# article.__dict__.keys()
# article.meta_keywords
# df.columns

# news = df.web_url.apply(NewsPlease.from_url)

# url = "https://www.nytimes.com/2011/12/22/world/asia/hong-kong-culls-chickens-after-bird-flu-is-found.html"

new = NewsPlease.from_url(url)
maindf = pd.json_normalize(news.apply(lambda s: s.__dict__))  # .maintext.iloc[0]
maindf.to_csv("nyt_full.csv")
