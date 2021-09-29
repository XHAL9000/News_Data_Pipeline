from bs4 import BeautifulSoup
import requests
from lxml import etree
from headers import header_list
import random
from RedisProxyPool.RedisProxy import ProxyRecord

class ContentParser():
    def __init__(self,link,proxy_record):
        self.link = link 
        self.proxy_record = proxy_record

    def getHTML(self,timeout=30):
        article = self.getRequest()
        soup = BeautifulSoup(article.content, 'html.parser')
        dom = etree.HTML(str(soup))
        return dom

    def getRequest(self):
        kwargs = {
            "timeout": 30,
            "headers": random.choice(header_list),
            "proxies" : self.proxy_record.proxy
        }
        article = requests.get(self.link, **kwargs) 
        return article
    
    def getText(self):
        article = self.getHTML()
        if "france24" in self.link:
            dom = article.xpath("/html/body/main/div[3]/article/div[6]//p//text()")
        if "francetv" in self.link:
            dom = article.xpath('/html/body/main/article/div[6]//p//text()')
        return dom
    
