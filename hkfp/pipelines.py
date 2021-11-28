# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from datetime import datetime
import logging
import os
import json

class BadScrapePipeline:
    def open_spider(self, spider):
        self.datetimenow = datetime.now().strftime("%Y%m%d_%H%M%S")
        badfilepath = f"data/badfiles/{self.datetimenow}.jl"
        if not os.path.exists("data/badfiles"):
            os.makedirs("data/badfiles")     
        self.file = open(badfilepath, "w")
        # open bad files folder 

    def Attrcheck(self, item, attr):
        if not item.get(attr):
            line = json.dumps(ItemAdapter(item).asdict()) + "\n"
            self.file.write(line)
            raise DropItem(f"No {attr} in {item}")

    def process_item(self, item, spider):
        # if doesn't have fields, send to badfiles folder
        req_attrs = ["Body", "Headline"]
        for attr in req_attrs:
            self.Attrcheck(item, attr) 
        return item

    def close_spider(self, spider):
        self.file.close()
