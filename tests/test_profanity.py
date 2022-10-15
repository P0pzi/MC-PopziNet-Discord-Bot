from unittest import TestCase

from modules.profanity import ProfanityModule
from tests.mocks import MockMessage

sentences_test = [
    # Sentence, is bad sentence
    ("This sentence doesn't contain a bad word.", False),
    ("This sentence contains the word fuck", True),
    ("Ass and hole equals asshole", True),
    ("Assessment of this sentence should say its not a bad sentence", False),
    ("You look like a fuckhead", True),
    ("You need an assfuck", True),
    ("You fUckER!!!!", True),
    ("awww crap!", False),
    ("cunt", True),
    ("A$$fucker", True)
]


class ProfanityTests(TestCase):

    profanity_module = ProfanityModule()

    def test_all_sentences_on_badness(self):
        for (sentence, isBad) in sentences_test:

            self.profanity_module.reset()
            self.profanity_module.set_message(
                MockMessage(sentence)
            )
            self.profanity_module.check()

            self.assertEqual(
                self.profanity_module.has_profane_words,
                isBad,
                sentence
            )
