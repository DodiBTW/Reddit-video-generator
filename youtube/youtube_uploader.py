import os
import pickle
from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

class YouTubeUploader:
    def __init__(self):
        # Load environment variables from .env file
        load_dotenv()

        # Get the client secrets file path from the environment variable
        client_secrets_path = os.getenv("CLIENT_SECRET_PATH")
        
        if not client_secrets_path:
            raise ValueError("CLIENT_SECRET_PATH is not set in the .env file")

        # Ensure the path to the client secrets file is correct relative to the script's location
        client_secrets_path = os.path.join(os.path.dirname(__file__), '../', client_secrets_path)

        self.credentials = self._authenticate(client_secrets_path)

        # Initialize the YouTube API service
        self.youtube = build("youtube", "v3", credentials=self.credentials)

    def _authenticate(self, client_secrets_path):
        """Authenticate the user using OAuth 2.0"""
        SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

        # Check if token.pickle exists (cached credentials)
        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                credentials = pickle.load(token)
        else:
            # Run OAuth flow if no token exists
            flow = InstalledAppFlow.from_client_secrets_file(client_secrets_path, SCOPES)
            credentials = flow.run_local_server(port=0)
            
            # Save the credentials for the next time
            with open("token.pickle", "wb") as token:
                pickle.dump(credentials, token)

        return credentials

    def upload_video(self, video_file, title, description, privacy_status="public"):
        """Upload a video to YouTube"""
        media = MediaFileUpload(video_file, mimetype="video/*", resumable=True)

        request = self.youtube.videos().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": title,
                    "description": description,
                    "tags": ["#shorts"],
                    "categoryId": "22",  # You can adjust this if needed
                },
                "status": {
                    "privacyStatus": privacy_status,  # "public", "private", or "unlisted"
                },
            },
            media_body=media,
        )

        response = request.execute()
        return response

    def get_channels(self):
        """Get the authenticated user's YouTube channel(s)"""
        request = self.youtube.channels().list(
            part="snippet,contentDetails,statistics",
            mine=True
        )
        response = request.execute()
        
        channels = []
        for channel in response['items']:
            channels.append({
                "channel_name": channel['snippet']['title'],
                "channel_id": channel['id'],
                "channel_description": channel['snippet']['description']
            })
        return channels
