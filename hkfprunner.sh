#!/bin/bash
source activate env/bin/activate
# FOR HKFP ENTIRE CORPUS
scrapy crawl hkfp -O hkfp_full.csv

# manually upload hkfp_full.csv to newyorktime/hkfp/hkfp_full.csv