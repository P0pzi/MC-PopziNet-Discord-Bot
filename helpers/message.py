from functools import lru_cache


@lru_cache(maxsize=None)
def cleanup_word(word: str) -> str:
    """
    Replaces leet speak characters to regular characters
    :param word: The word that needs cleaning up
    """
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

    for char, replacement in replacements.items():
        word = word.replace(char, replacement)

    return word


@lru_cache(maxsize=None)
def split_sentence(sentence: str) -> list:
    """
    Take a sentence and return a list of words in it
    :param sentence: the sentence to split up
    """
    return [word for word in sentence.split(" ")]


@lru_cache(maxsize=None)
def split_cleanup_sentence(sentence: str) -> list:
    """
    Take a sentence and return a cleanup list of words in it
    :param sentence: the sentence to clean and split
    """
    split = split_sentence(sentence)
    return [cleanup_word(word) for word in split]
