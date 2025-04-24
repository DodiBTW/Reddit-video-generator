import math
import re

class DataExtractor:
    def __init__(self, data):
        self.data = data
        print(data)

    def extract_post_content(self):
        dict = {}
        title = self.data[0]["data"]["children"][0]["data"]["title"]
        selftext = self.data[0]["data"]["children"][0]["data"]["selftext"]

        link_pattern = re.compile(r'\[.*?\]\(.*?\)')
        title = re.sub(link_pattern, '', title)
        selftext = re.sub(link_pattern, '', selftext)

        dict["title"] = title.replace(" ", "  ").replace("\n", "  ")
        dict["selftext"] = selftext.replace(" ", "  ").replace("\n", "  ")
                
        return dict
    def extract_short_post_content(self, title, selftext):
        dict = {}
        link_pattern = re.compile(r'\[.*?\]\(.*?\)')
        title = re.sub(link_pattern, '', title)
        selftext = re.sub(link_pattern, '', selftext)

        dict["title"] = title.replace(" ", "  ").replace("\n", "  ")
        dict["selftext"] = selftext.replace(" ", "  ").replace("\n", "  ")
                
        return dict
    def extract_comments(self, num_comments = 0, all = False):
        comments = []
        if num_comments > self.count_comments() or all == True:
            num_comments = self.count_comments()
        print("Number of comments that will be taken is : ", num_comments)
        for i in range(num_comments):
            if self.data[1]["data"]["children"][i]["data"]["body"] not in ["" , "[deleted]" , "[removed]", None]:
                comments.append(self.data[1]["data"]["children"][i]["data"]["body"])
        return comments

    def count_comments(self):
        return len(self.data[1]["data"]["children"])