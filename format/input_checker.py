class InputChecker:
    def __init__(self):
        pass
    def check_link(self, link):
        if "reddit" not in link or "." not in link or "https://" not in link or "/" not in link:
            return False
        return True