from typing import List, Dict
from text_alignment_tool.alignment_algorithms import AlignmentAlgorithm, local_alignment
from text_alignment_tool.shared_classes import (
    LetterList,
    TextAlignments,
)
import swalign
import numpy as np

# from alignment_tool import AlignmentTextPair, AlignmentRange
from text_alignment_tool.find_wordlist_for_alignment import find_wordlist_for_alignment


class NeedleInHaystackAlgorithm(AlignmentAlgorithm):
    """The Rough Alignment Algorithm is intended to help find a relatively
    small query text within a very large target text. It uses several techniques
    to speed up the search process so that a long running local or global
    alignment process can be avoided.

    """

    def __init__(self, chunk_split_token: str = " "):
        self.chunk_split_token = ord(chunk_split_token)
        super().__init__()

    def align(self) -> TextAlignments:
        # Find the words in target that are most unique to search against
        # query_text = self._query
        # target_text = self._target

        tokenized_query_text: List[LetterList] = []
        current_query_text_chunk = []
        query_full_to_tokenized_map: Dict[int, List[int]] = {}
        for idx, entry in zip(range(self._query.size), np.nditer(self._query)):

            if len(tokenized_query_text) not in query_full_to_tokenized_map:
                query_full_to_tokenized_map[len(tokenized_query_text)] = []
            query_full_to_tokenized_map[len(tokenized_query_text)].append(idx)

            if entry == self.chunk_split_token:
                tokenized_query_text.append(np.array(current_query_text_chunk))
                current_query_text_chunk = []
                continue

            current_query_text_chunk.append(entry)

        last_tmp_chunk = np.array(current_query_text_chunk)
        if not np.array_equal(tokenized_query_text[-1], last_tmp_chunk):
            tokenized_query_text.append(last_tmp_chunk)

        tokenized_target_text: List[LetterList] = []
        current_target_text_chunk = []
        target_full_to_tokenized_map: Dict[int, List[int]] = {}
        for idx, entry in zip(range(self._target.size), np.nditer(self._target)):

            if len(tokenized_target_text) not in target_full_to_tokenized_map:
                target_full_to_tokenized_map[len(tokenized_target_text)] = []
            target_full_to_tokenized_map[len(tokenized_target_text)].append(idx)

            if entry == self.chunk_split_token:
                tokenized_target_text.append(np.array(current_target_text_chunk))
                current_target_text_chunk = []
                continue

            current_target_text_chunk.append(entry)

        last_tmp_chunk = np.array(current_target_text_chunk)
        if not np.array_equal(tokenized_target_text[-1], last_tmp_chunk):
            tokenized_target_text.append(last_tmp_chunk)

        hashed_query_text: LetterList = np.array(
            [int_array_hash(x) for x in tokenized_query_text], dtype=np.uint32
        )
        hashed_target_text: LetterList = np.array(
            [int_array_hash(x) for x in tokenized_target_text], dtype=np.uint32
        )
        unique_tokens_in_texts = np.unique(
            np.concatenate([hashed_query_text, hashed_target_text])
        )
        combined_text_hash = {x: idx for idx, x in enumerate(unique_tokens_in_texts)}
        less_common_text_words = find_wordlist_for_alignment(hashed_target_text, 100)

        unique_target_text_matching_word_codes = {}
        query_text_token_codes = []
        for line_element in hashed_query_text:
            if line_element not in less_common_text_words:
                continue

            target_text_matches = [
                idx for idx, x in enumerate(hashed_target_text) if x == line_element
            ]
            word_code = combined_text_hash[line_element]
            query_text_token_codes.append(word_code)
            for target_text_match in target_text_matches:
                unique_target_text_matching_word_codes[
                    f"{target_text_match}_{word_code}"
                ] = {"index": target_text_match, "wordcode": word_code}

        if not unique_target_text_matching_word_codes.values():
            return self._alignment

        (rough_start_in_target_text, rough_end_in_target_text,) = rough_alignment(
            hashed_target_text,
            less_common_text_words,
            query_text_token_codes,
            combined_text_hash,
        )

        query_text_length = len(hashed_query_text)

        # Take the rough match and extend the search outward by half the length of the query string on each side
        padded_match_start = max(
            0, int(rough_start_in_target_text - (query_text_length / 2))
        )
        padded_match_end = min(
            len(hashed_target_text),
            int(rough_end_in_target_text + (query_text_length / 2)),
        )

        start_full_target_idx = target_full_to_tokenized_map[padded_match_start][0]
        end_full_target_idx = target_full_to_tokenized_map[padded_match_end][-1]

        # Get a local alignment
        local_alignment_attempt = local_alignment(
            self._query,
            self._target[start_full_target_idx:end_full_target_idx],
            target_offset=start_full_target_idx,
        )

        self._alignment = local_alignment_attempt

        return super().align()


def rough_alignment(
    target_text, unique_target_text_matching_word_codes, query_word_codes, text_hash
):
    alignment_word_codes = [
        text_hash[x] for x in target_text if x in unique_target_text_matching_word_codes
    ]

    # choose your own values here… 2 and -1 are common.
    match = 2
    mismatch = -1
    scoring = swalign.NucleotideScoringMatrix(match, mismatch)

    sw = swalign.LocalAlignment(scoring)  # you can also choose gap penalties, etc...
    target_text_symbolic_transcription = "".join([chr(x) for x in alignment_word_codes])
    query_symbolic_transcription = "".join([chr(x) for x in query_word_codes])
    alignment = sw.align(
        target_text_symbolic_transcription, query_symbolic_transcription
    )
    start_idx, end_idx = alignment.r_pos, alignment.r_end
    alignment.dump()
    return start_idx, end_idx


# TODO: find a better hashing algorithm
def int_array_hash(l: LetterList) -> int:
    # Input is an array of uint32, so we set the max size accordingly and hope not to get collisions
    max_int_size = 2 ** 32

    acc = 1
    for a, b in zip(l, l[-1:] + l[:-1]):
        acc += acc * int(a) - int(b)
    return (acc + max_int_size) % max_int_size
