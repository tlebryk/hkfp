# %%
import urllib
import re
import xml.etree.ElementTree as ET 
import requests
import time
import os
import pandas as pd
# %%
tree = ET.parse("data\sitemap\master_sitemap.xml")
root = tree.getroot()
# %%
# get archive dates for file naming purposes
# prefix being removed is: https://hongkongfp.com/
substr= ".com/"
ind= root[0][0].text.index(substr)
start = ind + len(substr)
counter = 0
for item in root: 
    response =requests.get(item[0].text)
    if response != 200:
        print("error: page didn't load:" + item[0].text[start:])
    filepath = 'data/sitemap/childsitemaps/'+item[0].text[start:]
    with open(filepath, 'wb') as f:
        f.write(response.content)
    counter +=1
    time.sleep(5)
# %%
# SITEMAPS TO csvs of urls

# move irrelevant xmls to respective folders
path = "data/sitemap/childsitemaps"
for f in os.listdir(path):
    if not os.path.exists(f"{path}/newspack"):
        os.makedirs(f"{path}/newspack/")

    if "newspack" in f:
        os.rename(f"{path}/{f}", f"{path}/newspack/{f}")
    elif not os.path.exists(f"{path}/post_tag"):
        os.makedirs(f"{path}/post_tag/")
    elif "post_tag" in f:
        os.rename(f"{path}/{f}", f"{path}/post_tag/{f}")
    elif not os.path.exists(f"{path}/post-sitemap"):
        os.makedirs(f"{path}/post-sitemap/")
    elif "post-sitemap" in f:
        os.rename(f"{path}/{f}", f"{path}/post-sitemap/{f}")
    elif not os.path.exists(f"{path}/product/"):
        os.makedirs(f"{path}/product")
    elif "product" in f:
        os.rename(f"{path}/{f}", f"{path}/product/{f}")
    elif not os.path.exists(f"{path}/misc"):
        os.makedirs(f"{path}/misc/")
    elif "page-sitemap" in f or \
        "category-sitemap" in f or \
        "post_format-sitemap" in f or \
        "author-sitemap" in f:
        os.rename(f"{path}/{f}", f"{path}\misc\{f}")


# %%
path = "data/sitemap/childsitemaps/post-sitemap"
dctls = []
for f in os.listdir(path):
    tree = ET.parse(f"{path}\{f}")
    root = tree.getroot()
    for r in root:
        dct = {
            'url': r[0].text,
            'date':  r[1].text,
            'sourcefile': f, 
        }
        dctls.append(dct)
pd.DataFrame(dctls).to_csv("data/urls/posts.csv")

    # urls.append(url)


# %%
