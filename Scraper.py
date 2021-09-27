
import feedparser
import pandas as pd
from bs4 import BeautifulSoup
import requests
from lxml import etree
from headers import header_list
import random
import streamlit as st

class FeedParser():

    def __init__(self,url):
        self.url = url
        self.proxylist =  open('proxylist.txt').read().split('\n')
        self.content = self.parse()
        

    def parse(self):
        parsedRSS = feedparser.parse(self.url)
        df_parse = pd.DataFrame(columns=['id','link', 'title', 
                       'content', 'time'])
        df_list = [{'id' : news["id"], 'link' : news["link"],'title' : news["summary"]
                 ,'content': self.getText(news["link"]) ,'time': news["published_parsed"]}
                  for news in parsedRSS['entries']]
        df_parse = df_parse.append(df_list)
        return df_parse                

    def getRequest(self,link):
        proxy = random.choice(self.proxylist)
        kwargs = {
            "timeout": 30,
            "headers": random.choice(header_list)
        }

        try :
            kwargs["proxies"] = {'http': 'http://' +proxy}
            article = requests.get(link, **kwargs)
        except:
            self.proxylist.remove(proxy)
            proxy = random.choice(self.proxylist)
        return article

    def getText(self,link,timeout=30,proxies=None):

        article = self.getRequest(link)
        soup = BeautifulSoup(article.content, 'html.parser')
        dom = etree.HTML(str(soup))
        dom = dom.xpath("/html/body/main/div[3]/article/div[6]/p")
        text = [p.text for p in dom  ]
        return text
        
        
