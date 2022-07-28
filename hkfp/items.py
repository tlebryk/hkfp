# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field
from dataclasses import dataclass


@dataclass
class ArticleItem:
    Date: str
    Art_id: str
    Search_url: str
    Original_url: str
    Response_url: str
    Headline: str  # headline as displayed on page
    Title: str  # from title meta at top of page; often contains - Globaltimes
    Author: str
    Topics: list
    Body: str
    Section: str
    # VADER_neg: float
    # VADER_neu: float
    # VADER_pos: float
    # VADER_compound: float
    feed: str = ""
    clean_title: str = ""
    dislikes: int = 0
    likes: int = 0
    message: str = ""
    ratingsEnabled: str = ""  # really bool
    isSpam: str = ""  # really bool
    isDeleted: str = ""  # really bool
    category: int = 0
    adsDisabled: str = ""  # really bool
    authorid: int = 0
    threadid: int = 0
    signedLink: str = ""
    createdAt: str = ""  # really datetime in format: 2021-12-20T18:11:07,
    hasStreaming: str = ""  # really bool
    raw_message: str = ""
    isClosed: str = ""  # really bool
    link: str = ""
    slug: str = ""
    forum: str = ""
    identifier: str = ""


@dataclass
class CommentItem:
    editableUntil: str
    dislikes: int
    thread: int
    numReports: int
    likes: int
    message: str
    id: int
    createdAt: str
    commenterid: int  # get author id and turn rest into commenter element
    postid: int
    # identifier: str


@dataclass
class CommenterItem:
    # remember to deduplicate at some point in the pipeline
    username: str
    about: str
    name: str
    disable3rdPartyTrackers: str  # really bool
    isPowerContributor: str  # really bool
    joinedAt: str
    profileUrl: str
    url: str
    location: str
    isPrivate: str  # really bool
    signedUrl: str
    isPrimary: str
    isAnonymous: str
    id: int  # must convert beforehand
