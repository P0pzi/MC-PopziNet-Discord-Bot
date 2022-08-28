import random
import discord

from string import Template

from helpers.message import split_cleanup_sentence
from static.admins import Admins
from static.rooms import ChatRooms
from tests.mocks import MockMessage

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

    def __init__(self):
        self.message = None
        self.profanity = []

    @property
    def profane_word_count(self) -> int:
        return len(self.profanity)

    @property
    def has_profane_words(self) -> bool:
        return self.profane_word_count > 0

    @property
    def unique_words(self) -> list:
        lowercase_sentence = self.message.content.lower()
        cleaned_sentence_part = split_cleanup_sentence(lowercase_sentence)
        return list(set(cleaned_sentence_part))

    def set_message(self, message: [discord.Message, MockMessage]) -> "Profanity":
        self.message = message
        return self

    def reset(self) -> "Profanity":
        self.message = None
        self.profanity = []
        return self

    def check(self) -> None:
        """
        Doesn't check messages coming from ignored rooms or users, and identifies bad words contained
        in the current message. Always checks in MOD_DEVELOPMENT_BOT channel for development purposes
        :return: None
        """

        if self.message.channel.id != ChatRooms.MOD_DEVELOPMENT_BOT.value and (
                self.message.channel.id in Profanity.IGNORE_ROOMS
                or self.message.author.id in Profanity.IGNORE_USERS
        ):
            return

        self.profanity = self.get_profanity()

    def get_profanity(self) -> list:
        found_profanity = [
            profane_word.removeprefix("*").removesuffix("*") for profane_word in bad_words
            if self.is_profane_word_in_message(profane_word)
        ]

        return list(set(found_profanity))

    def is_profane_word_in_message(self, profane_word: str) -> bool:
        """
        Determines if a profane word is contained in a sentence
        :param profane_word: A word that is considered profane
        """

        profane_word_without_asterisks = profane_word.removeprefix("*").removesuffix("*")

        if profane_word.startswith("*") and profane_word.endswith("*"):
            return any(profane_word_without_asterisks in word for word in self.unique_words)

        elif profane_word.startswith("*"):
            return any(word.endswith(profane_word_without_asterisks) for word in self.unique_words)

        elif profane_word.endswith("*"):
            return any(word.startswith(profane_word_without_asterisks) for word in self.unique_words)

        return any(needle_word == profane_word_without_asterisks for needle_word in self.unique_words)

    def get_message_reply(self) -> str:
        """
        Generates a reply when bad words are detected in the current message
        """
        if self.profane_word_count <= 0:
            # Something is wrong with the code if someone sees this.
            return "Your message is clean. Good job."

        words = ""
        if self.profane_word_count == 1:
            words = Template(singular_bad_word).substitute(word=self.profanity[0])
        elif self.profane_word_count > 1:
            words = Template(multiple_bad_words).substitute(words=", ".join(self.profanity))

        followup = random.choice(funny_followups)

        return Template(badwords_message).substitute(
            bad_words=words,
            followup=followup
        )
