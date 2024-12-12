import re
class Subtitles:
    def __init__(self, title, body, speed = 160):
        """
            title = title of the reddit post, extracted during request
            body = content of the reddit post, extracted during request
            Speed = speaking speed of the tts agent (wpm)
        """
        self.title = title
        self.body = body
        self.speed = speed
    def get_speaking_duration(self, text):
        split_text = [word for word in re.split(r'\s+|[.]', text) if word]
        period_count = text.count('.')+ text.count(';') + text.count('?') + text.count('!')
        comma_count = text.count(',') + text.count('(') + text.count(')') + text.count(':')
        return len(split_text) / (self.speed / 60) + (0.4 * comma_count)+ (0.5 * period_count)
    def get_subtitle_array_into_subtitles(self, array, initial_time = 0):
        subtitles = []
        current_time = initial_time
        for text in array:
            duration = self.get_speaking_duration(text)
            subtitles.append((duration, text, current_time))
            current_time += duration
        print("total duration: ", current_time)
        return subtitles
    def divide_text_into_sentences(self, text, char_amount=50):
        """
            char_amount is the amount of maximum characters to be allowed in one array split(aka subtitle on screen simultaneously)
        """
        words = text.split()
        subtitles = []
        current_selection = ""
        i = 0
        while i < len(words):
            if len(words[i]) > char_amount:
                subtitles.append(words[i])
                i += 1
            else:
                current_selection = words[i]
                if i + 1 < len(words) and len(current_selection) + len(words[i + 1]) + 1 <= char_amount:
                    current_selection += " " + words[i + 1]
                    if i + 2 < len(words) and len(current_selection) + len(words[i + 2]) + 1 <= char_amount:
                        current_selection += " " + words[i + 2]
                        i += 3
                    else:
                        i += 2
                else:
                    i += 1
                subtitles.append(current_selection)
        return subtitles

    def get_divided_body(self, char_amount = 80):
        return self.divide_text_into_sentences(self.body, char_amount)
    def add_line_breaks(text, max_chars=20):
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