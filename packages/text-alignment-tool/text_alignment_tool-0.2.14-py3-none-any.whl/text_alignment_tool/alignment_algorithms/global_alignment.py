import logging
from minineedle import needle
from minineedle.core import Gap
from text_alignment_tool.alignment_algorithms import AlignmentAlgorithm
from text_alignment_tool.shared_classes import (
    LetterList,
    TextChunk,
    TextAlignments,
    AlignmentKey,
)


class GlobalAlignmentAlgorithm(AlignmentAlgorithm):
    def __init__(self, chunked: bool = False):
        super().__init__()
        self.__chunked_alignment = chunked

    def align(self) -> TextAlignments:
        if self._alignment.alignments:
            return self._alignment

        if self.__chunked_alignment:
            self._output_query_text_chunk_indices = self._input_query_text_chunk_indices
            self._output_target_text_chunk_indices = (
                self._input_target_text_chunk_indices
            )
            self._alignment = global_chunked_alignment(
                self._query,
                self._target,
                self._input_query_text_chunk_indices,
                self._input_target_text_chunk_indices,
            )
        if not self.__chunked_alignment:
            self._output_query_text_chunk_indices = self._input_query_text_chunk_indices
            self._output_target_text_chunk_indices = (
                self._input_target_text_chunk_indices
            )
            _, self._alignment = global_alignment(self._query, self._target)
        return self._alignment


def global_chunked_alignment(
    query_text: LetterList,
    target_text: LetterList,
    query_text_chunks: list[TextChunk],
    target_text_chunks: list[TextChunk],
) -> TextAlignments:
    alignments = TextAlignments()

    if len(query_text_chunks) != len(target_text_chunks):
        logging.warning(
            f"Since the query has {len(query_text_chunks)} text chunks and the target has {len(target_text_chunks)}, the alignment will probably not work as intended."
        )

    query_start_end = [(x.indices[0], x.indices[-1]) for x in query_text_chunks]
    target_start_end = [(x.indices[0], x.indices[-1]) for x in target_text_chunks]
    for (query_start_idx, query_end_idx), (target_start_idx, target_end_idx) in zip(
        query_start_end, target_start_end
    ):
        query_text_chunk = query_text[query_start_idx:query_end_idx]
        target_text_chunk = target_text[target_start_idx:target_end_idx]
        _, results = global_alignment(query_text_chunk, target_text_chunk)
        alignments.alignments = alignments.alignments + results.alignments

    return alignments


def global_alignment(
    query_text: LetterList,
    target_text: LetterList,
) -> tuple[int, TextAlignments]:
    alignments = TextAlignments()
    alignment = needle.NeedlemanWunsch(query_text, target_text)
    alignment.align()
    al1, al2 = alignment.get_aligned_sequences("list")
    query_idx = -1
    target_idx = -1
    for query_entity, target_entity in zip(al1, al2):
        query_is_gap = isinstance(query_entity, Gap)
        target_is_gap = isinstance(target_entity, Gap)

        if not query_is_gap:
            query_idx += 1
        if not target_is_gap:
            target_idx += 1

        if query_is_gap or target_is_gap:
            continue

        alignments.alignments.append(AlignmentKey(query_idx, target_idx))

    return (alignment.get_score(), alignments)
