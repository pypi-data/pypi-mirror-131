import logging
from text_alignment_tool.alignment_algorithms import (
    AlignmentAlgorithm,
    global_alignment,
)
from text_alignment_tool.shared_classes import (
    TextChunk,
    LetterList,
    TextAlignments,
    AlignmentKey,
)
import itertools
import numpy as np


class LocalAlignmentAlgorithm(AlignmentAlgorithm):
    def __init__(self):
        super().__init__()

    def align(self) -> TextAlignments:
        """
        Perform a local alignment of the query and target.  Primarily
        this is useful for finding a small chunk of query text within
        a large chunk of target text. It will probably not be able to
        provide a good  alignment on the letter level, but it should be
        quite close on the chunk level. The output of
        `output_query_text_chunk_indices` and
        `output_target_text_chunk_indices` can be used to find a more
        precise global alignment.
        """

        alignments = local_alignment(self._query, self._target)
        self._alignment = alignments
        return self._alignment

        if len(self._input_query_text_chunk_indices) != len(
            self._input_target_text_chunk_indices
        ):
            logging.warning(
                f"Since the query has {len(self._input_query_text_chunk_indices)} text chunks and the target has {len(self._input_target_text_chunk_indices)}, the alignment will probably not work as intended."
            )

        # output_query_chunks: list[TextChunk] = []
        # output_target_chunks: list[TextChunk] = []
        # query_start_end = [
        #     (x.indices[0], x.indices[-1]) for x in self._input_query_text_chunk_indices
        # ]
        # target_start_end = [
        #     (x.indices[0], x.indices[-1]) for x in self._input_target_text_chunk_indices
        # ]
        # for (query_start_idx, query_end_idx), (target_start_idx, target_end_idx) in zip(
        #     query_start_end, target_start_end
        # ):
        #     alignments = local_alignment(
        #         self._query[query_start_idx : query_end_idx + 1],
        #         self._target[target_start_idx : target_end_idx + 1],
        #     )
        #     output_query_chunks.append(
        #         TextChunk(list(range(alignments[0], alignments[1])), "")
        #     )
        #     output_target_chunks.append(
        #         TextChunk(list(range(alignments[2], alignments[3])), "")
        #     )

        output_query_chunks = self._input_query_text_chunk_indices.copy()
        output_target_chunks = self._input_target_text_chunk_indices.copy()

        # Note that these alignments will probably not be very good
        text_alignments: list[AlignmentKey] = []
        chunk_matches: list[tuple[TextChunk, TextChunk]] = []
        for query_chunk in output_query_chunks:
            best_match_score = len(query_chunk.indices)  # worst possible score
            for target_chunk in output_target_chunks:
                alignments, score = global_alignment(
                    self._query[query_chunk.indices], self._target[target_chunk.indices]
                )
                if score < best_match_score:  # We want the lowest score
                    best_match_score = score
                    best_match = (query_chunk, target_chunk)
            pass

        for query_chunk, target_chunk in zip(output_query_chunks, output_target_chunks):
            max_target_idx = target_chunk.indices[-1] + 1
            for idx in range(query_chunk.indices[-1] - query_chunk.indices[0] + 1):
                query_idx = query_chunk.indices[0] + idx
                target_idx = (
                    target_chunk.indices[0] + idx
                    if target_chunk.indices[0] + idx < max_target_idx
                    else max_target_idx
                )
                text_alignments.append(AlignmentKey(query_idx, target_idx))

        # Save alignments to self object
        self._output_query_text_chunk_indices = output_query_chunks
        self._output_target_text_chunk_indices = output_target_chunks
        self._alignment.alignments = text_alignments

        return super().align()


def local_alignment(
    query_text: LetterList,
    target_text: LetterList,
) -> TextAlignments:
    start, end = smith_waterman(query_text, target_text, 10, 2)
    _, alignments = global_alignment(query_text, target_text[start : end + 1])
    alignments.alignments = [
        AlignmentKey(x.query_idx, x.target_idx + start) for x in alignments.alignments
    ]
    return alignments


# Adapted from https://tiefenauer.github.io/blog/smith-waterman/
def matrix(a, b, match_score=3, gap_cost=2):
    H = np.zeros((a.size + 1, b.size + 1), dtype=np.int32)

    for i, j in itertools.product(range(1, H.shape[0]), range(1, H.shape[1])):
        match = H[i - 1, j - 1] + (
            match_score if a[i - 1] == b[j - 1] else -match_score
        )
        delete = H[i - 1, j] - gap_cost
        insert = H[i, j - 1] - gap_cost
        H[i, j] = max(match, delete, insert, 0)
    return H


def traceback(H, b, b_=0, old_i=0, end_match=0):
    # Optimized for tail call recursion
    while True:
        # flip H to get index of **last** occurrence of H.max() with np.argmax()
        H_flip = np.flip(np.flip(H, 0), 1)
        i_, j_ = np.unravel_index(H_flip.argmax(), H_flip.shape)
        i, j = np.subtract(
            H.shape, (i_ + 1, j_ + 1)
        )  # (i, j) are **last** indexes of H.max()
        if H[i, j] == 0:
            return b_, j
        b_ = b[j - 1].size + 1 + b_ if old_i - i > 1 else b[j - 1].size + b_
        H = H[0:i, 0:j]


def traceback_simple(H, end_match=0):
    # Optimized for tail call recursion
    while True:
        # flip H to get index of **last** occurrence of H.max() with np.argmax()
        H_flip = np.flip(np.flip(H, 0), 1)
        i_, j_ = np.unravel_index(H_flip.argmax(), H_flip.shape)
        i, j = np.subtract(
            H.shape, (i_ + 1, j_ + 1)
        )  # (i, j) are **last** indexes of H.max()
        if H[i, j] == 0:
            return end_match, j
        H = H[0:i, 0:j]

        if end_match == 0:
            end_match = j


def smith_waterman(a, b, match_score=3, gap_cost=2):
    H = matrix(a, b, match_score, gap_cost)
    # b_, pos = traceback(H, b)
    end, start = traceback_simple(H)
    return start, end
