import format.text_logger as text_logger
import format.input_checker as input_checker
import reddit_helper.reddit as reddit
import reddit_helper.data_extractor as data_extractor
import video.video as video
import tts.speech_generator as speech_generator
if __name__ == "__main__":
    logger = text_logger.TextLogger()
    checker = input_checker.InputChecker()
    logger.log("Welcome to the reddit video generator!", open = True)
    logger.log("Please enter the link to the reddit post you want to generate a video for.")
    logger.log("Please note that the link must be a reddit post link and not a direct link to the video.")
    logger.log("For example: https://www.reddit.com/r/aww/6xkz8o/this_is_my_dog/")
    logger.log("Please enter the link below:", close = True)
    link = ""
    while True:
        try:
            link = str(input("Enter the link: ")).strip()
            if not checker.check_link(link):
                raise Exception
            break
        except:
            logger.clear_console()
            logger.log("Invalid link. Please enter a valid link.", open=True, close=True)
    logger.log("Link accepted!", open=True)
    logger.log("Please enter the title of the video you want to generate.", close=True)
    title = ""
    while True:
        try:
            title = str(input("Enter the title: ")).strip()
            break
        except:
            logger.clear_console()
            logger.log("Invalid title. Please enter a valid title.", open=True, close=True)
    logger.close_log()
    logger.log("Title accepted!", open=True)
    if link.endswith("/"):
        link = link[:-1]
    link = link + ".json"
    reddit_extractor = reddit.Reddit(link)
    logger.log("Fetching data from reddit...", open=True)
    data = reddit_extractor.fetchData()
    logger.log("Data fetched successfully!", close=True)
    extractor = data_extractor.DataExtractor(data)
    logger.log("Extracting post information...", open=True)
    content = extractor.extract_post_content()
    body = content["selftext"]
    post_title = content["title"]
    logger.log("Extracted post information!", close=True)
    logger.log("Generating text to speech...", open=True)
    tts_manager = speech_generator.SpeechGenerator()
    tts_manager.save_body_tts(body)
    tts_manager.save_title_tts(post_title)
    logger.log("Text to speech generated successfully!", close=True)
    logger.log("Generating video...", open=True)
    video_manager = video.Video(title, post_title, body, audio_delay=1.5)
    video_manager.create_video(True)
    logger.log("Video generated successfully!", close=True)
    logger.log("Thank you for using the reddit video generator!", open=True, close=True)