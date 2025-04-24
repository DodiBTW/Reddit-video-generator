import json
import os
import random
import time
from reddit_helper.reddit import Reddit
from reddit_helper.data_extractor import DataExtractor
from video.video import Video
from tts.speech_generator import SpeechGenerator
from youtube.youtube import upload_video
if not os.path.exists("env"):
    os.makedirs("env")

def load_used_posts():
    if not os.path.exists("env/used_posts.json"):
        with open("env/used_posts.json", "w") as f:
            json.dump([], f)
    try:
        with open("env/used_posts.json", "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # If the file is empty or contains invalid JSON, reset it to an empty list
        with open("env/used_posts.json", "w") as f:
            json.dump([], f)
        return []

def save_used_post(post_id):
    used_posts = load_used_posts()
    used_posts.append(post_id)
    with open("env/used_posts.json", "w") as f:
        json.dump(used_posts, f)

def load_subreddits():
    if not os.path.exists("env/subreddits.json"):
        with open("env/subreddits.json", "w") as f:
            json.dump(["funny", "aww", "gaming", "pics"], f)
    with open("env/subreddits.json", "r") as f:
        return json.load(f)

def main():
    while True:
        subreddits = load_subreddits()
        subreddit = random.choice(subreddits)
        reddit = Reddit(f"https://www.reddit.com/r/{subreddit}/hot.json")
        posts = reddit.fetch_popular_posts(subreddit)
        generated = False
        used_posts = load_used_posts()

        for post in posts:
            if not reddit.check_post_valid(post):
                continue

            post_id = post['data']['id']
            if post_id in used_posts:
                continue
            data_extractor = DataExtractor([post])
            content = data_extractor.extract_short_post_content(post['data']['title'], post['data']['selftext'])
            body = content["selftext"]
            title = content["title"]
            print(f"Generating subtitles for post: {title} from {subreddit}")
            tts_manager = SpeechGenerator()
            tts_manager.save_body_tts(body)
            tts_manager.save_title_tts(title)
            print()
            print("Generating video for post...")
            video_manager = Video(title, title, body, audio_delay=1.5)
            video_manager.create_video(True)

            video_name = video_manager.get_file_path()
            upload_video(video_name, title=title, desc=body)

            save_used_post(post_id)
            generated = True
            break
        if not generated:
            print("No valid posts found. Retrying in 3 seconds...")
            time.sleep(3)
        else:
            time.sleep(30)
if __name__ == "__main__":
    main()