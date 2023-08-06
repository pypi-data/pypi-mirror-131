import requests


class HetuCounter:
    def __init__(self, url=''):
        self.url = url if url else 'http://47.110.94.96:5000/hetu/api/counter'
        self.token = 'eHVlbGFuZ3l1bg=='
        self.req_count()

    def req_count(self):
        requests.get(url=self.url)
        return 1
