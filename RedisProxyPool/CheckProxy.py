from dataclasses import dataclass
from ProxyPool import ProxyRecord
from NewsScraper.ArticleScraper import ContentParser
import time
import requests

@dataclass(frozen=True)
class ProxyStatus:
    proxy: str
    health: float
    is_valid: bool

class ProxyChecker : 
    def __init__(self, url, timeout=10, checks=10, sleep_interval=0.1):
        self.timeout = timeout
        self.checks = checks
        self.sleep_interval = sleep_interval
        self.parser= ContentParser(url)
    
    def check_proxy(self, proxy_record):
        total_checks = []
        for i in range(self.checks):
            response = self.parser.getRequest().content
            time.sleep(self.sleep_interval)
            total_checks.append(int(response is not None))
        health = self.checks/sum(total_checks)
        proxy_status = ProxyStatus(
            proxy_record.proxy,
            health,
            health > 0.7
        )
        return proxy_status
