
import redis
import json


class RedisProxyPool:
    def __init__(self,key,redis_conn):
        self.redis_conn = redis_conn
        self.key = key

    def add_proxies(self,proxies):
        self.redis_conn.delete(self.key)
        self.redis_conn.lpush(self.key,*proxies)
    def get_proxies(self):
        proxies = self.redis.lrange(self.key,0,-1)
        return [json.loads(proxy) for proxy  in proxies]

    def get_proxy(self):
        proxies = self.get_proxies()
        if len(proxies>0):
            return proxies[0]
    def lpop(self):
        self.redis.lpop(self.key)
    def __exit__(self):
        client_id = self.redis_conn.clirnt_id()
        self.redis_conn.client_kill_filter(_id = client_id)
