import requests as requests
import json
import time
import os
import sys
import platform
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'format')))
import text_logger as text_logger
class Reddit:
    def __init__(self, link):
        self.url = link
        self.logger = text_logger.TextLogger()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
        }
    def fetchData(self):
        try:
            response = requests.get(self.url, headers = self.headers)
            response.raise_for_status()
            return response.json()
        except:
            self.logger.log(f"Failed to fetch data for link {self.url}. Please check the link or website status and try again.", close = True)
            exit()