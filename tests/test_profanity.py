from unittest import TestCase

from models.message import Message
from modules.profanity import Profanity

sentences_test = [
    # Sentence, is bad sentence
    ("This sentence doesn't contain a bad word.", False),
    ("This sentence contains the word fuck", True),
    ("Ass and hole equals asshole", True),
    ("Assessment of this sentence should say its not a bad sentence", False),
    ("You look like a fuckhead", True),
    ("You need an assfuck", True),
    ("You fUckER!!!!", True),
    ("awww crap!", True),
    ("cunt", True),
    ("A$$fucker", True)
]


class ProfanityTests(TestCase):
    def test_all_sentences_on_badness(self):
        for (sentence, isBad) in sentences_test:
            message_words = Message.split_message(sentence)
            bad_words = Profanity.get_profanity(message_words)
            self.assertEqual(len(bad_words) > 0, isBad, sentence)
