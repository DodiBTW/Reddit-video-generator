import requests as requests
import os
import sys
import re

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
    def fetch_popular_posts(self, subreddit, limit=100):
        url = f"https://www.reddit.com/r/{subreddit}/hot.json?limit={limit}"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            posts = data['data']['children']
            return posts
        else:
            self.logger.log(f"Failed to fetch popular posts from subreddit {subreddit}.", close = True)
            exit()
    def check_post_valid(self, post, char_limit=2500):
        # we need the post to be text post with no images or videos just a story
        if post['data']['is_video'] == True or post['data']['is_reddit_media_domain'] == True:
            return False
        if post['data']['is_self'] == False:
            return False
        if post['data']['selftext'] == "" or post['data']['selftext'] == "[deleted]" or post['data']['selftext'] == "[removed]":
            return False
        if post['data']['title'] == "" or post['data']['title'] == "[deleted]" or post['data']['title'] == "[removed]":
            return False
        body = post['data']['selftext']
        link_pattern = re.compile(r'\[.*?\]\(.*?\)')
        body = re.sub(link_pattern, "", body)
        if len(body) > char_limit:
            return False
        return True