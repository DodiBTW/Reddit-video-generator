class DataExtractor:
    def __init__(self, data):
        self.data = data
    def extract_post_content(self):
        dict = {}
        dict["title"] = self.data[0]["data"]["children"][0]["data"]["title"]
        dict["selftext"] = self.data[0]["data"]["children"][0]["data"]["selftext"]
        return dict
    def extract_comments(self, num_comments):
        comments = []
        for i in range(num_comments):
            # giving error if list out of range
            if self.data[1]["data"]["children"][i]["data"]["body"] not in ["" , "[deleted]" , "[removed]", None]:
                comments.append(self.data[1]["data"]["children"][i]["data"]["body"])
        return comments