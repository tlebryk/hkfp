import json
import scrapy
import logging
from html_text import extract_text
import re
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from datetime import datetime
import os

# from selenium import webdriver
from hkfp.items import CommenterItem, CommentItem, ArticleItem

CURRENTDIR = os.getcwd()
DATETIMENOW = datetime.now().strftime("%Y%m%d_%H%M%S")
LOGPATH = f"{CURRENTDIR}/logs/globaltimes/"
if not os.path.exists(LOGPATH):
    os.makedirs(LOGPATH)
logging.basicConfig(
    filename=f"{LOGPATH}/{DATETIMENOW}.log",
    format="%(asctime)s %(levelname)-8s  %(filename)s %(lineno)d %(message)s",
    level=logging.INFO,
    datefmt="%Y-%m-%d %H:%M:%S",
)

sid = SentimentIntensityAnalyzer()



class GlobaltimesSpider(scrapy.Spider):
    name = "globaltimes"
    # allowed_domains = ["globaltimes.cn"]
    start_urls = ["https://search.globaltimes.cn/QuickSearchCtrl?search_txt=hong+kong"]
    custom_settings = {
        "FEEDS": {
            f"s3://globaltimes/data/allscrape_{datetime.now().strftime('%Y%m%d_%H%M%S')}": {
                "format": "csv",
                "encoding": "utf8",
            }
        }
    }
    # def __init__(self, name=None, **kwargs):
    #     self.uri = "s3://globaltimes/data/allscrape_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    #     super().__init__(name=name, **kwargs)

    def parse(self, response):
        lastpg = int(response.css("a.btn::text").getall()[-3].strip())
        for i in range(1, lastpg)[:2]:  # TODO: delete [:] which constrains for testing
            url = f"https://search.globaltimes.cn/QuickSearchCtrl?page_no={i}&search_txt=hong+kong"
            logging.info(f"Working on {url}")
            yield scrapy.Request(url=url, callback=self.parse_search)

    def parse_search(self, response):
        logging.info(f"parse_searching {response.url}")
        articles = response.css("div.row-fluid:not(.pages):not(.body-fluid)")
        for art in articles[:2]: # TODO: remove [] which controls/ limits rate. 
            url = art.css("a::attr(href)").get()
            date = art.css("small")
            if date:
                date = extract_text(date.get())
                index = date.find("Source")
                if index != -1:
                    date = date[:index].strip()
            if url:
                # self.driver.get(url)

                # self.driver.close()
                yield response.follow(
                    url, callback=self.page_parse, cb_kwargs={"date": date}
                )
            else:
                logging.warning("could not find url for page...")

    def page_parse(self, response, date):
        logging.info(f"pageparsing {response.url}")
        original_url = response.request.meta.get("redirect_urls", response.request.url)
        Response_url = response.request.url
        result = re.search("(.*)/(.*).shtml", Response_url)
        try:
            art_id = result.group(2)
        except:
            logging.warning(f"could not find id in url, leaving as null")
            art_id = ""
        title = extract_text(
            response.css("title").get()
        )  # title we need for disqus request
        headline = extract_text(
            response.css("div.article_title").get()
        )  # headline we need for vader
        vader = sid.polarity_scores(headline)
        article = ArticleItem(
            Date=date,
            Art_id=art_id,
            Original_url=response.request.meta.get(
                "redirect_urls", response.request.url
            ),
            Response_url=response.request.url,
            Headline=headline,
            Author=response.css("meta#MetaAuthor::attr(content)").get(),
            Title=title,
            # haven't found any multi author pieces...
            Topics=(
                extract_text(response.css("div.span9.text-muted").get())
                .removeprefix("Posted in:")
                .strip()
            ),
            Body=extract_text(response.css("div.article_content").get()),
            VADER_neg=vader["neg"],
            VADER_neu=vader["neu"],
            VADER_pos=vader["pos"],
            VADER_compound=vader["compound"],
        )
        commenturl = f"https://disqus.com/embed/comments/?base=default&f=globaltimes&t_i={art_id}&t_u={Response_url}&t_d={title}&t_t={title}&s_o=default"
        yield response.follow(
            commenturl, callback=self.comments_parse, cb_kwargs=dict(article=article)
        )

    def comments_parse(self, response, article):
        logging.info(f"starting comment parse on {response.url}")
        scripts = response.css("script")
        for script in scripts:
            innerhtml = script.xpath("string(.)").get()  # get inner html
            try:
                data = json.loads(innerhtml)
                if data.get("response"):
                    break
            except:
                continue  # if script not json try next script
        if not data.get("response"):
            logging.error(f"Could not find comment json data...?")
            return None
        r = data["response"]
        thread = r["thread"]
        article.feed = thread["feed"]
        article.clean_title = thread["clean_title"]
        article.dislikes = int(thread["dislikes"])
        article.likes = int(thread["likes"])
        article.message = thread["message"]
        article.ratingsEnabled = thread["ratingsEnabled"]
        article.isSpam = thread["isSpam"]
        article.isDeleted = thread["isDeleted"]
        article.category = int(thread["category"])
        article.adsDisabled = thread["adsDisabled"]
        article.authorid = int(thread["author"])
        article.threadid = int(thread["id"])
        article.signedLink = thread["signedLink"]
        article.createdAt = thread["createdAt"]
        article.hasStreaming = thread["hasStreaming"]
        article.raw_message = thread["raw_message"]
        article.isClosed = thread["isClosed"]
        article.link = thread["link"]
        article.slug = thread["slug"]
        article.forum = thread["forum"]
        yield article
        posts = r["posts"]
        for post in posts:
            comment = CommentItem(
                editableUntil=post["editableUntil"],
                dislikes=int(post["dislikes"]),
                thread=int(post["thread"]),
                numReports=int(post["numReports"]),
                likes=int(post["likes"]),
                message=post["message"],
                id=int(post["id"]),
                createdAt=post["createdAt"],
                commenterid=int(post["author"]["id"]),
            )
            yield comment
            auth = post["author"]
            commenter = CommenterItem(
                username=auth["username"],
                about=auth["about"],
                name=auth["name"],
                disable3rdPartyTrackers=auth["disable3rdPartyTrackers"],
                isPowerContributor=auth["isPowerContributor"],
                joinedAt=auth["joinedAt"],
                profileUrl=auth["profileUrl"],
                url=auth["url"],
                location=auth["location"],
                isPrivate=auth["isPrivate"],
                signedUrl=auth["signedUrl"],
                isPrimary=auth["isPrimary"],
                isAnonymous=auth["isAnonymous"],
                id=int(auth["id"]),
            )
            yield commenter


# response.xpath("//div[contains(class, 'ratings')]")