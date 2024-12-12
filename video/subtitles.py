import re
class Subtitles:
    def __init__(self, title, body, speed = 140):
        """
            Speed = speaking speed of the tts agent (wpm)
        """
        self.title = title
        self.body = body
        self.speed = speed
    def get_speaking_duration(self, text):
        split_text = [word for word in re.split(r'\s+|[.]', text) if word]
        return len(split_text) / (self.speed / 60)
    def get_subtitle_array_into_subtitles(self, array, initial_time = 0):
        subtitles = []
        current_time = initial_time
        for text in array:
            duration = self.get_speaking_duration(text)
            subtitles.append((duration, text, current_time))
            current_time += duration
        return subtitles
    def divide_text_into_sentences(self, text, char_amount= 35):
        """
            char_amount is the amount of maximum characters to be allowed in one array split(aka subtitle on screen simultaneously)
        """
        sentences = re.split(r'(?<=[.!?;])\s+', text.strip())
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
    def get_divided_body(self, char_amount = 60):
        return self.divide_text_into_sentences(self.body, char_amount)
    def add_line_breaks(text, max_chars=25):
        """
        Inserts a newline character into the text every `max_chars` characters without breaking words.
        """
        words = text.split()
        current_line = ""
        lines = []

        for word in words:
            if len(current_line) + len(word) + 1 <= max_chars:  # +1 for the space
                current_line += (word + " ")
            else:
                lines.append(current_line.strip())
                current_line = word + " "  # Start new line with the current word

        if current_line:
            lines.append(current_line.strip())  # Add the remaining text

        return "\n".join(lines)