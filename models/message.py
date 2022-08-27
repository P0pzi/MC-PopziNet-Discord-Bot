
class Message:

    def __init__(self):
        self.WORDS = None
        self.WORDS_UPPER = None
        self.WORDS_LOWER = None
        self.VALUE = None
        self.CHANNEL = None
        self.AUTHOR = None
        self.PROFANITY = False
        self.BAD_WORDS = []

    def __str__(self):
        return self.VALUE

    @property
    def bad_word_count(self):
        return len(self.BAD_WORDS)

    @property
    def is_profane(self):
        return self.bad_word_count > 0

    @staticmethod
    def cleanup_word(word):
        replacements = {
            "@": "a",
            "$": "s",
            "0": "o",
            "3": "e",
            "4": "a",
            "+": "t",
            "7": "t",
            "?": "",
            "!": "",
            ".": "",
            ",": "",
        }

        word = word.lower()
        for char, replacement in replacements.items():
            word = word.replace(char, replacement)
        return word

    @staticmethod
    def split_message(message):
        return [Message.cleanup_word(word) for word in message.split(' ')]
