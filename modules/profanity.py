import random
import discord

from string import Template

from static.admins import Admins
from static.rooms import ChatRooms
from static.currentMessage import CurrentMessage

bad_words = open("./static/badwords.txt", "r").read().splitlines()
bad_words = [word.lower() for word in bad_words]

badwords_message = "Please keep the chat clean ($bad_words), else $followup... \N{SERIOUS FACE WITH SYMBOLS COVERING MOUTH}"
singular_bad_word = "Bad word: $word"
multiple_bad_words = "Bad words: $words"

funny_followups = [
    "I'll rip your friggin' arms off",
    "I'll hang you by your toenails on the clothes line",
    "I'll make your body stand still and your head do a 360",
    "I'll put you on a rocket and shoot you into outer space",
    "I'll have your mom do my laundry",
    "you'll get to sleep without socks on tonight"
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

    # Keep the last / current message in memory
    def __init__(self):
        self._current_message = None

    def is_bad_word_in_message(self, bad_word):
        """
        Determines if a bad word is contained in the current message
        :param bad_word: An entry from badwords.txt
        :return: list or string
        """
        fixed_bad_word = bad_word.removeprefix("*").removesuffix("*")

        if bad_word.startswith("*") and bad_word.endswith("*"):
            return any(fixed_bad_word in needle_word for needle_word in self.current_msg.WORDS_LOWER)
        elif bad_word.startswith("*"):
            return any(needle_word.endswith(fixed_bad_word) for needle_word in self.current_msg.WORDS_LOWER)
        elif bad_word.endswith("*"):
            return any(needle_word.startswith(fixed_bad_word) for needle_word in self.current_msg.WORDS_LOWER)

        return any(needle_word == fixed_bad_word for needle_word in self.current_msg.WORDS_LOWER)

    def check(self):
        """
        Doesn't check messages coming from ignored rooms or users, and identifies bad words contained
        in the current message.
        :return: None
        """
        if self.current_msg.CHANNEL.id in Profanity.IGNORE_ROOMS and \
                self.current_msg.CHANNEL.id != ChatRooms.MOD_DEVELOPMENT_BOT.value:
            return

        if self.current_msg.AUTHOR.id in Profanity.IGNORE_USERS and \
                self.current_msg.AUTHOR.id != ChatRooms.MOD_DEVELOPMENT_BOT.value:
            return

        # Remove dupes by making a set first, then turning it into a list again
        self.current_msg.BAD_WORDS = list(
            set(
                [
                    bad_word.removeprefix("*").removesuffix("*") for bad_word in bad_words
                    if self.is_bad_word_in_message(bad_word)
                ]
            )
        )

    def get_message_reply(self):
        """
        Generates a reply when bad words are detected in the current message
        :return:
        """
        if self.current_msg.bad_word_count <= 0:
            # Something is wrong with the code if someone sees this.
            return "Your message is clean. Good job."

        words = ""
        if self.current_msg.bad_word_count == 1:
            words = Template(singular_bad_word).substitute(word=self.current_msg.BAD_WORDS[0])
        elif self.current_msg.bad_word_count > 1:
            words = Template(multiple_bad_words).substitute(words=", ".join(self.current_msg.BAD_WORDS))

        followup = random.choice(funny_followups)

        return Template(badwords_message).substitute(
            bad_words=words,
            followup=followup
        )

    @property
    def current_msg(self):
        return self._current_message

    @current_msg.setter
    def current_msg(self, discord_message):
        if type(discord_message) is not discord.Message:
            raise TypeError("Current message is not of a discord type")
        self._current_message = CurrentMessage()
        self._current_message.VALUE = discord_message
        self._current_message.WORDS = [word for word in discord_message.content.split(' ')]
        self._current_message.WORDS_LOWER = [word.lower() for word in self._current_message.WORDS]
        self._current_message.WORDS_UPPER = [word.upper() for word in self._current_message.WORDS]
        self._current_message.CHANNEL = discord_message.channel
        self._current_message.AUTHOR = discord_message.author
        self.check()
