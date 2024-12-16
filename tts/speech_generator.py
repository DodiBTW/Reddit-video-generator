from gtts import gTTS
import os

class SpeechGenerator:
    def __init__(self, language='en'):
        self.language = language
        self.accent = 'com'
        self.save_path = "temp"
        
        os.makedirs(self.save_path, exist_ok=True)

    def save_title_tts(self, text):
        output_file = os.path.join(self.save_path, 'temporary_title_audio.mp3')
        tts = gTTS(text=text, lang=self.language, slow=False)
        tts.save(output_file)

    def save_body_tts(self, text):
        output_file = os.path.join(self.save_path, 'temporary_body_audio.mp3')
        tts = gTTS(text=text, lang=self.language, slow=False)
        tts.save(output_file)