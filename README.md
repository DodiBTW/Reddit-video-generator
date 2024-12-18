# Reddit video generator
 Python script which will generate 9:16 format videos from reddit stories, with generative text to speech and algorithmic subtitles.
## Isn't it beautiful?
This python script will generate a well structured reddit video format which is currently very popular on platforms like tiktok and youtube shorts, fully automatically! The process of thousands of different channels can be automated and generated in a few minutes once a day for the same results.

How? Just run the script and enter a link, as well as the title of your video, and you will receive a full reddit video after a few moments!

## How this script works
- The script uses the requests library to pull the reddit data, then formats it into a title and a body.
- Calls the gtts (Google text-to-speech) api which is a free, account-less api that will generate realistic text to speech voices.
- Uses some estimation functions to assume how long a video will last, divides the body into small parts for subtitles, and calculates approximately how long each one will take to be read, ensuring an accurate text to speech representation.
- Chooses a random video from the assets/videos folder, then cuts it randomly based on total duration of text to speech.
- Adds speech and subtitles onto the video with correct timings and delays
- Renders the video
## How to use
Install python 3, as well as all dependencies in the requirements.txt file, then add videos to the assets/videos folder. Afterwards, you can simply run main.py 
