from string import Template

from static.admins import Admins
from static.rooms import ChatRooms

badwords = open("./static/badwords.txt", "r").read().splitlines()

badwords_message = "Please keep the chat clean ($bad_words), $followup"
singular_bad_word = "Bad word: $word"
multiple_bad_words = "Bad words: $words"

# TODO Add more random funny followups
funny_followups = [
    'else I\'ll rip your friggin\' arms off. \N{SERIOUS FACE WITH SYMBOLS COVERING MOUTH}'
]


class Profanity:

    # Chat won't be checked in these rooms
    IGNORE_ROOMS = [
        ChatRooms.MOD_CHAT.value,
        ChatRooms.MOD_ALERTS.value,
        ChatRooms.MOD_LOGS.value,
        ChatRooms.MOD_DEVELOPMENT.value
    ]

    # Chat won't be checked for these users
    IGNORE_USERS = [
        # Add user ID's here.
        # Admins are added automatically
    ] + [admin.value for admin in Admins]

    def __init__(self, message):
        self.message = message
        self.channel = message.channel
        self.author = message.author

        self.message_words = [word.lower() for word in self.message.content.split(' ')]
        self.bad_words = [word.lower() for word in badwords]

        self.checked = False
        self.profanity = []

        self.check()

    def is_bad_word_in_message(self, bad_word):
        if bad_word.startswith("*") and bad_word.endswith("*"):
            return any(needle_word in bad_word for needle_word in self.message_words)
        elif bad_word.startswith("*"):
            return any(needle_word.endswith(bad_word) for needle_word in self.message_words)
        elif bad_word.endswith("*"):
            return any(needle_word.startswith(bad_word) for needle_word in self.message_words)
        return any(needle_word is bad_word for needle_word in self.message_words)

    def check(self):
        if self.channel.id in Profanity.IGNORE_ROOMS and self.channel.id != ChatRooms.MOD_DEVELOPMENT_BOT.value:
            return

        if self.author.id in Profanity.IGNORE_USERS and self.channel.id != ChatRooms.MOD_DEVELOPMENT_BOT.value:
            return

        # Remove dupes by making a set first, then turning it into a list again
        self.profanity = list(
            set(
                [
                    bad_word for bad_word in self.bad_words
                    if self.is_bad_word_in_message(bad_word)
                ]
            )
        )
        self.checked = True

    def get_message_reply(self):
        if self.bad_word_count <= 0:
            # Something is wrong with the code if someone sees this.
            return "Your message is clean. Good job."

        if self.bad_word_count == 1:
            words = Template(singular_bad_word).substitute(word=self.profanity[0])
        elif self.bad_word_count > 1:
            words = Template(multiple_bad_words).substitute(words=", ".join(self.profanity))
        else:
            words = ""

        # TODO Get random funny follow up
        followup = funny_followups[0]

        return Template(badwords_message).substitute(
            bad_words=words,
            followup=followup
        )

    @property
    def has_profanity(self):
        return self.checked and self.bad_word_count > 0

    @property
    def bad_word_count(self):
        return len(self.profanity)
