import math
class DataExtractor:
    def __init__(self, data):
        self.data = data
    def extract_post_content(self):
        dict = {}
        dict["title"] = self.data[0]["data"]["children"][0]["data"]["title"]
        dict["selftext"] = self.data[0]["data"]["children"][0]["data"]["selftext"]
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