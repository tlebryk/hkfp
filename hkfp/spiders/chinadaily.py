import json
import logging
import os
import re
from datetime import datetime

import scrapy

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


class ChinaDailySpider(scrapy.Spider):
    name = "chinadaily"
    # allowed_domains = ["globaltimes.cn"]
    query = "alibaba"
    start_url = "https://newssearch.chinadaily.com.cn/rest/en/search?publishedDateFrom=2011-01-01&publishedDateTo=2021-12-31&fullMust={}&channel=&type=&curType=story&sort=dp&duplication=on&page={}&type[0]=story&channel[0]=2@cndy&channel[1]=2@webnews&channel[2]=2@bw&channel[3]=2@hk&channel[4]=ismp@cndyglobal&source="
    errors = []
    # custom_settings = {
    #     "FEEDS": {
    #         f"s3://globaltimes/data/allscrape_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv": {
    #             "format": "csv",
    #             "encoding": "utf8",
    #         },
    #         f"data/allscrape_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv": {
    #             "format": "csv",
    #             "encoding": "utf8",
    #         },
    #     }
    # }
    # uri = f"s3://globaltimes/data/allscrape_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    # def __init__(self, name=None, **kwargs):
    #     self.uri = "s3://globaltimes/data/allscrape_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    #     super().__init__(name=name, **kwargs)

    def start_requests(self):
        # lastpg = 4753  # from prior research for hl=k
        # lastpg = 803 idk where this was from
        lastpg = 756
        for i in range(1, lastpg + 1):  # TODO: delete [:] which constrains for testing
            url = self.start_url.format(self.query, i)
            logging.info(f"Working on %s", url)
            yield scrapy.Request(
                url=url, callback=self.parse_search, cb_kwargs={"pg_num": i}
            )

    def parse_search(self, response, pg_num):
        """Get article urls from a search page"""
        # pg_num = self.get_pg_num(response.url)
        logging.info("working on %s", pg_num)
        if response.status != 200:
            error_dct = {"pg_num": pg_num, "url": response.url, "code": response.status}
            if pg_num:
                logging.warning("%s returns status code %s", pg_num, response.status)
            self.errors.append(error_dct)
        dct = response.json()
        content = dct.pop("content")
        for c in content:
            yield (c)
        if not os.path.exists("china_daily_meta11.json"):
            with open("china_daily_meta11.json", "w") as f:
                json.dump(dct, f)


"""
dict_keys(['id', 'inner_id', 'title', 'keywords', 'tags', 'source', 'url', 'content', 'created', 'publishTime', 'plainText', 'updated', 'system', 'lastModified', 'authors', 'author_low', 'type', 'subtitle', 'originalId', 'summary', 'channelId', 'channelName', 'columnName', 'attIds', 'img', 'extInfo', 'dupTitle', 'dupFlag', 'categories', 'storyType', 'thumbnailStyle', 'contentType', 'canComment', 'wordCount', 'imageCount', 'leadinLine', 'shareUrl', 'images', 'jsonUrl', 'thumbnails', 'columnDirname', 'mediaStream', 'resources', 'properties', 'language', 'comment', 'editor', 'reviewEditor', 'originUrl', 'originUri', 'expired', 'specialId', 'editorRecommends', 'originSpecialId', 'columnId', 'highlight', 'highlightTitle', 'highlightContent', 'pubDateStr'])
"""
