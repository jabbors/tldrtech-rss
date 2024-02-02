# -*- coding: utf-8 -*-
import re
from urllib.request import urlopen
from urllib.error import HTTPError, URLError
from datetime import datetime
from email import utils
from bs4 import BeautifulSoup
from article import Article

class Parser:

    page = None
    pageUrl = None
    articles = []

    def __init__(self, date):
        # self.pageUrl = "https://tldr.tech/api/latest/tech"
        self.pageUrl = "https://tldr.tech/tech/" + date
        self.articles = []

    def timeNowRfc822(self):
        return utils.format_datetime(datetime.now())

    def getPage(self):
        try: response = urlopen(self.pageUrl)
        except (URLError, HTTPError, e):
            return e
        self.page = response.read().decode('utf-8')
        return None
    
    def parseArticles(self):
        soup = BeautifulSoup(self.page)
        # find content-center div
        contentCenterDiv = soup.findAll('div', {'class':'content-center'})
        if len(contentCenterDiv) == 0:
            return "no content div found"
        if len(contentCenterDiv[0].contents) == 0:
            return "content div is empty"
        # find all mt-3 divs
        mt3Divs = contentCenterDiv[0].findAll('div', {'class':'mt-3'})
        if len(mt3Divs) == 0:
            return "no articles found"
        for div in mt3Divs:
            # find article link
            a = div.findAll('a')
            # find article body div
            c = div.findAll('div')
            if len(a) == 0 and len(c) == 0:
                # article does not contain a link nor a div element
                continue
            # find article title
            t = a[0].findAll('h3')
            if len(t) == 0:
                # link does not contain a title
                continue
            article = Article(t[0].contents[0], c[0].contents[0], a[0].get('href'))
            self.articles.append(article)
        return None

    def generateFeed(self, file):
        if len(self.articles) == 0:
            return "no articles have been parsed"
        rss = self.generateFeedStart()
        for article in self.articles:
            rss += article.generateRssItem()
        rss += self.generateFeedEnd()
        f = open(file, "w")
        f.write(rss)
        f.close()
        return None
    
    def generateFeedStart(self):
        feed = '''<rss version="2.0">
<channel>
<title>TLDR news</title>
<link>https://tldr.tech/</link>
<description>TLDR RSS</description>
<pubDate>DATE_PLACEHOLDER</pubDate>
'''
        return feed.replace("DATE_PLACEHOLDER", self.timeNowRfc822())

    def generateFeedEnd(self):
        feed = '''</channel>
</rss>
'''
        return feed