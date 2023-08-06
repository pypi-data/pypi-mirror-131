from itertools import groupby
from typing import Counter, Union, List, Dict, Tuple
import numpy as np
import re
from bidict import bidict

from text_alignment_tool.shared_classes.shared_classes import LetterList


# See https://stackoverflow.com/questions/4998629/split-string-with-multiple-delimiters-in-python
def split(delimiters: List[str], string: str, maxsplit: int = 0) -> List[str]:
    regexPattern = "|".join(map(re.escape, delimiters))
    return re.split(regexPattern, string, maxsplit)


def letter_list_to_unique_word_codes(
    letter_list: np.ndarray, separators: Union[List[str], None] = None
) -> Tuple[np.ndarray, bidict[str, int], Dict[int, List[int]]]:
    """
    This assigns a unique number to each unique word in the submitted
    text. It returns an array with the text represented by its unique
    word codes along with the word_code_key.
    """

    parsed_separators = separators if separators is not None else [" "]

    indexed_text = [(chr(x), idx) for idx, x in enumerate(letter_list)]
    word_chunks = (
        list(g)
        for k, g in groupby(indexed_text, key=lambda x: x[0] not in parsed_separators)
        if k
    )
    word_map: Dict[str, int] = {}
    coded_output: List[int] = []
    word_to_letter_map: Dict[int, List[int]] = {}
    current_word_idx = 0
    for idx, word in enumerate(word_chunks):
        text_word = "".join([x[0] for x in word])
        if text_word not in word_map:
            word_map[text_word] = current_word_idx
            current_word_idx = current_word_idx + 1
        coded_output.append(word_map[text_word])
        word_to_letter_map[idx] = [x[1] for x in word]

    return (
        np.array(coded_output).astype(np.uint32),
        bidict(word_map),
        word_to_letter_map,
    )


def find_wordlist_for_alignment(
    input_gold_text: LetterList, max_word_frequency: int = 100
) -> LetterList:
    unique, frequency = np.unique(input_gold_text, return_counts=True)
    passing_frequency = frequency < max_word_frequency
    return unique[passing_frequency]


def filter_wordlist(
    wordlist: np.ndarray, valid_values: List[int]
) -> Tuple[np.ndarray, Dict[int, int]]:
    filtered_list = [(idx, x) for idx, x in enumerate(wordlist) if x in valid_values]
    return np.array([x[1] for x in filtered_list]).astype(np.uint32), {
        x[0]: idx for idx, x in enumerate(filtered_list)
    }
