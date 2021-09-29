from bs4 import BeautifulSoup
import requests
from dataclasses import dataclass



@dataclass
class ProxyRecord:
    ip_address: str
    port: int
    country_code: str
    country: str
    anonymity: str
    google: str
    https: str
    last_checked: str

    def __post_init__(self):
        self.proxy = self.format_proxy()

    def format_proxy(self):
        protocol = "https" if self.https == "yes" else "http"
        url = f"{protocol}://{self.ip_address}:{self.port}"
        return {"http": url, "https": url}


class ProxyPoolExtractor : 
    def __init__(self,url_ips):
        self.url_ips = url_ips

    def extract_proxies(self):
        ip_list = requests.get(self.url_ips)
        soup = BeautifulSoup(ip_list.content, 'lxml')
        ips_info = soup.find(id="list").find_all("tr")
        return [ip.find_all("td") for ip in ips_info]
    
    def get_proxies (self):
        proxies = self.extract_proxies()
        for proxy in proxies[1:]:
            yield  self.format_proxies(proxy)
            
    def format_proxies(self,proxy):
        return ProxyRecord(
            proxy[0].text, # ip address
            proxy[1].text,# port
            proxy[2].text, # code_country
            proxy[3].text,#code
            proxy[4].text,#anonimity
            proxy[5].text,#google
            proxy[6].text,#https
            proxy[7].text#last_checked
        )
