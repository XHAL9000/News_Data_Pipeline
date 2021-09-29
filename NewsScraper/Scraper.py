
import feedparser
import pandas as pd
from bs4 import BeautifulSoup
import requests
from lxml import etree
from headers import header_list
import random
import streamlit as st
from dataclasses import dataclass
from ArticleScraper import ContentParser


@dataclass(frozen=True)    
class News:
    _id: str
    title: str
    link: str
    published: str
    content: str
    
    def as_dict(self):
        return self.__dict__

class FeedParser():

    def __init__(self,url):
        self.url = url

    def parse(self):
        parsedRSS = feedparser.parse(self.url)
        for news in parsedRSS['entries'] :
            formatted_news = self.format_news(news)
            yield formatted_news

    def format_news(self,news):
        content = self.extract_content(news.link)
        return News(
            news.id,
            news.title,
            news.link,
            news.published,
            content
        )

    def extract_content(self,link):
        content =  ContentParser(link)
        return content.getText()



        

#rl = "https://www.france24.com/en/rss"
#for i in FeedParser("https://www.france24.com/en/rss").parse():
 #   print(i)