# Reddit video generator
 Python script which will generate 9:16 format videos from reddit stories, with generative text to speech and algorithmic subtitles.
## Isn't it beautiful?
This python script will generate a well structured reddit video format which is currently very popular on platforms like tiktok and youtube shorts, fully automatically! The process of thousands of different channels can be automated and generated in a few minutes once a day for the same results.

## How to use
- Install at least one video to the assets/videos folder in mp4 format.
- Install the python requirements from the requirement.txt file
- Run the script using python
- Paste a reddit post link
- Find generated video in the output folder

## How this script works
- The script uses the requests library to pull the reddit data, then formats it into a title and a body.
- Calls the gtts (Google text-to-speech) api which is a free, account-less api that will generate realistic text to speech voices.
- Uses some estimation functions to assume how long a video will last, divides the body into small parts for subtitles, and calculates approximately how long each one will take to be read, ensuring an accurate text to speech representation.
- Chooses a random video from the assets/videos folder, then cuts it randomly based on total duration of text to speech.
- Adds speech and subtitles onto the video with correct timings and delays
- Renders the video

## How to upload to youtube?
A new feature, uploading to YouTube, has been added.
In order to upload a video to youtube, you must create a google cloud console projet "Web app" and an Oauth2 client with "http://localhost:8080" allowed as a client. When you run the script with youtube video uploads, a tab will open on your browser where you can sign in to your account. Due to the fact our web app is still in test mode, you need to add your google account as a test user inside of the google cloud console web app. To do so, go to Apis and services > Oauth consent screen > Audience > Test users and add the email of your google account.

## Requirements
Install python 3, as well as all dependencies in the requirements.txt file, then add videos to the assets/videos folder. Afterwards, you can simply run main.py 
