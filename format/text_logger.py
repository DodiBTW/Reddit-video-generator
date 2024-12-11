import os
import platform
class TextLogger:
    def __init__(self):
        self.console_size = os.get_terminal_size()[0]
    def log(self, text , open = False, close = False, long = 120, little = 30):
        if open:
            self.open_log(long)
        print(("┃"+(long-2)*" "+"┃").center(self.console_size))
        print(("┃"+text.center(long-2)+"┃").center(self.console_size))
        print(("┃"+(long-2)*" "+"┃").center(self.console_size))
        if close:
            self.close_log(long)
        else:
            print(("┃"+(long-2)*" "+"┃").center(self.console_size))
            print(("┃"+(long-2)*"-"+"┃").center(self.console_size))
    def open_log(self, long = 120):
        print(("┏"+(long-2)*"━"+"┓").center(self.console_size))
        print(("┃"+(long-2)*" "+"┃").center(self.console_size))
    def close_log(self, long = 120):
        print(("┃"+(long-2)*" "+"┃").center(self.console_size))
        print(("┗"+(long-2)*"━"+"┛").center(60).center(self.console_size))
    def clear_console(self): 
        if platform.system() == "Windows":
            os.system('cls')
        else:
            os.system('clear')