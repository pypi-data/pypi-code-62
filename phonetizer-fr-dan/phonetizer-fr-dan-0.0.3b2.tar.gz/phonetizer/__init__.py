import re
import os

import pandas as pd

from phonetizer.utils.lexicon import load_lexicon


class WordNotFoundError(Exception):
    def __init__(self, word):
        super(WordNotFoundError, self).__init__(f"Word [{word}] was not found in Lexique.")
        
def word_to_phonem(word, dictionary):
    matches = dictionary.loc[lambda row: row.ortho == word].phon
    if matches.shape[0] == 0:
        raise WordNotFoundError(word)
    else:
        return matches.value_counts().index[0]

def sentence_to_phonem(sentence, dictionary: None):
    if dictionary is None:
        dictionary = load_lexicon()
    words = re.findall(r"[\w']+", sentence)
    phonems = [word_to_phonem(word, dictionary) for word in words]
    return ''.join(phonems)
