#!/bin/bash
source activate env/bin/activate

# find last page
# scrapy crawl chinadaily -O scratch12.jl -a year=2012
# # do full run
# scrapy crawl chinadaily -O cdaily12.jl -a year=2012
# python3 upload.py 2012

scrapy crawl chinadaily -O scratch16.jl -a year=2016
scrapy crawl chinadaily -O cdaily16.jl -a year=2016
python3 upload.py 2016

scrapy crawl chinadaily -O scratch17.jl -a year=2017
scrapy crawl chinadaily -O cdaily17.jl -a year=2017
python3 upload.py 2017


scrapy crawl chinadaily -O scratch18.jl -a year=2018
scrapy crawl chinadaily -O cdaily18.jl -a year=2018
python3 upload.py 2018

scrapy crawl chinadaily -O scratch19.jl -a year=2019
scrapy crawl chinadaily -O cdaily19.jl -a year=2019
python3 upload.py 2019

scrapy crawl chinadaily -O scratch20.jl -a year=2020
scrapy crawl chinadaily -O cdaily20.jl -a year=2020
python3 upload.py 2020

scrapy crawl chinadaily -O scratch21.jl -a year=2021
scrapy crawl chinadaily -O cdaily21.jl -a year=2021
python3 upload.py 2021