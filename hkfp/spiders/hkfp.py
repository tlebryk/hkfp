from datetime import datetime
import scrapy

# from nltk.sentiment.vader import SentimentIntensityAnalyzer

# import nltk
import pandas as pd
from html_text import extract_text
import logging
import os
from datetime import datetime

CURRENTDIR = os.getcwd()
DATETIMENOW = datetime.now().strftime("%Y%m%d_%H%M%S")
LOGPATH = f"{CURRENTDIR}/logs/hkfpspider/"
if not os.path.exists(LOGPATH):
    os.makedirs(LOGPATH)
logging.basicConfig(
    filename=f"{LOGPATH}/{DATETIMENOW}.log",
    format="%(asctime)s %(levelname)-8s  %(filename)s %(lineno)d %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)
# sid = SentimentIntensityAnalyzer()


class HKFPSpider(scrapy.Spider):
    name = "hkfp"
    try:
        start_urls = pd.read_csv(rf"data/urls/posts.csv").url.to_list()[:5]
    except:
        start_urls = []
    logging.info(start_urls)

    def parse(self, response):
        body = response.xpath('//div[@class="entry-content"]/p')
        body = "\n".join([extract_text(b.get()) for b in body])
        # try just getting all text from entry-content and not just p tags
        if not body:
            body = response.xpath('//div[@class="entry-content"]')
            body = "\n".join([extract_text(b.get()) for b in body])

        row = {
            "Date": response.xpath("//time/@datetime").get(),
            "Art_id": response.css("article::attr(id)").get(),
            "Original_url": response.request.meta.get(
                "redirect_urls", response.request.url
            ),
            "Response_url": response.request.url,
            "Headline": extract_text(response.xpath("//h1").get()),
            "Author": extract_text(
                response.css("span.author.vcard").get()
            ),  # haven't found any multi author pieces...
            "Topics": response.xpath('//span[@class="tags-links"]/a/text()').getall(),
            "Body": body,
        }
        # row["VADER_Compound"] = sid.polarity_scores(row["Headline"])["compound"]
        yield row


class ArticleSpider(scrapy.Spider):
    name = "article_spider"

    def __init__(self, *args, **kwargs):
        super(ArticleSpider, self).__init__(*args, **kwargs)

        self.start_urls = kwargs.pop("start_urls").split(",")
