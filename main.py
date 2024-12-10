import format.text_logger as text_logger
import format.input_checker as input_checker
import reddit_helper.reddit as reddit
import reddit_helper.data_extractor as data_extractor
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
    logger.log("How many comments would you like ", close=True)
    num_comments = 0
    while True:
        try:
            num_comments = int(input("Enter the number of comments: "))
            break
        except:
            logger.clear_console()
            logger.log("Invalid number of comments. Please enter a valid number.", open=True, close=True)
    if link.endswith("/"):
        link = link[:-1]
    link = link + ".json"
    reddit_extractor = reddit.Reddit(link)
    logger.log("Fetching data from reddit...", open=True)
    data = reddit_extractor.fetchData()
    logger.log("Data fetched successfully!", close=True)
    extractor = data_extractor.DataExtractor(data)
    logger.log("Extracting text and comments...", open=True)
    print(extractor.extract_post_content())
    print(extractor.extract_comments(num_comments))
    logger.log("Extracted text and comments!", close=True)
    logger.log("Generating video...", open=True)
    logger.log("Video generated successfully!", close=True)
    logger.log("Generating text to speech...", open=True)
    logger.log("Text to speech generated successfully!", close=True)
