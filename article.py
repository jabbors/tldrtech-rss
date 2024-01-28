# -*- coding: utf-8 -*-
class Article:
    title = None
    body = None
    link = None

    def __init__(self, title, body, link):
        self.title = str(title)
        self.body = str(body)
        self.link = str(link)

    def generateRssItem(self):
        item = "<item>\n"
        item += "<title>" + self.title + "</title>\n"
        item += "<description>" + self.body + "</description>\n"
        item += "<link>" + self.link + "</link>\n"
        item += "</item>\n"
        return item
