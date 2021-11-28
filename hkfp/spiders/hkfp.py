import scrapy
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd
from html_text import extract_text
sid = SentimentIntensityAnalyzer()



class HKFPSpider(scrapy.Spider):
    name = 'hkfp'

    start_urls = pd.read_csv(fr"C:\Users\tlebr\OneDrive - pku.edu.cn\Thesis\scmp\hkfp\data\urls\posts.csv").url.to_list()

    # def parse(self, response):
    #     # for pg in response.xpath('//article//h2//@href').getall():
    #     #     yield response.follow(pg, callback=self.parse_art)
    #     page = 2
    #     while True:
    #         x = scrapy.Request(response.urljoin("page/{}/".format(page)))
    #         if not x: 
    #             break
    #         page+=1
    #         print("page:", page)
    #         print("x", x)
    #     return page-1
    # def checker(self, response):
    #     if response.
        

    def parse(self,response):
        body = response.xpath('//div[@class="entry-content"]/p/text()')
        body = "\n".join([extract_text(b.get()) for b in body])

        row = {
            'Date': response.xpath('//time/@datetime').get(),
            "Art_id": response.css("article::attr(id)").get(), 
            "Url" : response.request.url,
            'Headline' : response.xpath('//h1/text()').get().strip(),
            'Author' : extract_text(response.css("span.author.vcard").get()), # haven't found any multi author pieces...
            'Topics': response.xpath('//span[@class="tags-links"]/a/text()').getall(),
            'Body' : body
        }
        row["VADER_Compound"]= sid.polarity_scores(row["Headline"])["compound"]
        yield row



class ArticleSpider(scrapy.Spider):
    name= "article_spider"

    def __init__(self, *args, **kwargs):
        super(ArticleSpider, self).__init__(*args, **kwargs)

        self.start_urls= kwargs.pop('start_urls').split(",")


        
# get urls from page:  
# response.xpath('//article//h2//@href').getall()
# get headline from page:
# response.xpath('//h1/text()').get()

# date: 
# response.xpath('//time/@datetime').get()

# tags
# response.xpath('//span[@class="tags-links"]/a/text()').getall()

# body
# response.xpath('//div[@class="entry-content"]/p/text()').getall()

# 