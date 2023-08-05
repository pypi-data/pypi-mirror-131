"""
   Handles symbol storage.
"""
from os import path, getcwd
from json import load

DEFAULT_SYMBOL_PATH = '../../data/phrasings.json'


class Symbols:
    """
    Hint:
        You can edit lists like additions, subtractions etc. to make a library's
        translation to other language (human language, not programming language)
        or implement any other custom behaviour you desire.

    Stores lists with words corresponding to given symbols.

    Args:
        path_to_phrasings:
            Stores path to .json file that has phrasing values.

    Attributes:
        symbol_dictionary:
            Stores all the symbol keys and their corresponding values.
    """

    def __init__(self, path_to_phrasings: str = DEFAULT_SYMBOL_PATH):
        if path_to_phrasings is DEFAULT_SYMBOL_PATH:
            actual_path = path.join(path.dirname(__file__), path_to_phrasings)
        else:
            actual_path = path.join(getcwd(), path_to_phrasings)
        with open(actual_path, encoding='UTF-8') as file:
            phrasings = load(file)

        self.symbol_dictionary = {
            '+': phrasings.get('additions'),
            '-': phrasings.get('subtractions'),
            '*': phrasings.get('multiplications'),
            '/': phrasings.get('divisions'),
            '**': phrasings.get('exponentiations'),
            'abs': phrasings.get('absolutes'),
            '%': phrasings.get('modulos'),
            'root': phrasings.get('roots'),
            '': phrasings.get('questions')
        }
