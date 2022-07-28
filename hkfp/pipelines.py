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
from scrapy.exporters import CsvItemExporter
from scrapy import signals
from datetime import datetime

DATETIMENOW = datetime.now().strftime("%Y%m%d_%H%M%S")


def item_type(item):
    return type(item).__name__.replace("Item", "").lower()  # TeamItem => team


class MultiCSVItemPipeline(object):
    SaveTypes = ["ArticleItem", "CommentItem", "CommenterItem"]

    def open_spider(self, spider):
        for name in self.SaveTypes:
            path = f"data/{spider.name}/{name}"
            if not os.path.exists(path):
                os.makedirs(path)
        self.files = dict(
            [
                (
                    name,
                    open(
                        f"data/{spider.name}/{name}/{spider.searchterm}_{DATETIMENOW}.csv",
                        "w+b",
                    ),
                )
                for name in self.SaveTypes
            ]
        )
        self.exporters = dict(
            [(name, CsvItemExporter(self.files[name])) for name in self.SaveTypes]
        )
        [e.start_exporting() for e in self.exporters.values()]

    def close_spider(self, spider):
        [e.finish_exporting() for e in self.exporters.values()]
        [f.close() for f in self.files.values()]

    def process_item(self, item, spider):
        whatype = type(item).__name__
        if whatype in set(self.SaveTypes):
            self.exporters[whatype].export_item(item)
        return item


class BadScrapePipeline:
    def open_spider(self, spider):
        self.datetimenow = datetime.now().strftime("%Y%m%d_%H%M%S")
        badfilepath = f"data/badfiles/{spider.name}"
        if not os.path.exists(badfilepath):
            os.makedirs(badfilepath)
        self.file = open(
            f"{badfilepath}/{spider.searchterm}_{self.datetimenow}.jl", "w"
        )
        # open bad files folder

    def Attrcheck(self, item, attr):
        if not ItemAdapter(item).asdict().get(attr):
            line = json.dumps(ItemAdapter(item).asdict()) + "\n"
            self.file.write(line)
            raise DropItem(f"No {attr} in {item}")

    def process_item(self, item, spider):
        # if doesn't have fields, send to badfiles folder
        whatype = type(item).__name__
        if whatype == "ArticleItem":
            req_attrs = ["Body", "Headline"]
            for attr in req_attrs:
                self.Attrcheck(item, attr)
        return item

    def close_spider(self, spider):
        self.file.close()
