#!/bin/bash
source activate env/bin/activate
# FOR HKFP ENTIRE CORPUS
scrapy crawl globaltimes -a searchterm='hong kong'
scrapy crawl globaltimes -a searchterm='alibaba'


# manually upload hkfp_full.csv to newyorktime/hkfp/hkfp_full.csv