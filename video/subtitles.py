import re
class Subtitles:
    def __init__(self, title, body, speed = 160):
        """
            Speed = speaking speed of the tts agent (wpm)
        """
        self.title = title
        self.body = body
        self.speed = speed
    def get_speaking_duration(self, text):
        split_text = [word for word in re.split(r'\s+|[.]', text) if word]
        return len(split_text) * (60/self.speed)
    def divide_text_into_sentences(self, text, char_amount= 60):
        """
            char_amount is the amount of maximum characters to be allowed in one array split(aka subtitle on screen simultaneously)
        """
        sentences = re.split(r'(?<=\.)\s+', text.strip())
        subtitles = []
        current_selection = ""
        for sentence in sentences:
            if current_selection == "" or len(current_selection) + len(sentence) < char_amount:
                if current_selection != "":
                    current_selection = current_selection + ". " + sentence
                else:
                    current_selection = sentence
            else:
                subtitles.append(current_selection)
                current_selection = sentence
        if current_selection != "":
            subtitles.append(current_selection)
        return subtitles
    def get_divided_title(self, char_amount = 60):
        return self.divide_text_into_sentences(self.title, char_amount)
    def get_divided_body(self, char_amount = 60):
        return self.divide_text_into_sentences(self.body, char_amount)