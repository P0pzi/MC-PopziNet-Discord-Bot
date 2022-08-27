
class CurrentMessage:

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

