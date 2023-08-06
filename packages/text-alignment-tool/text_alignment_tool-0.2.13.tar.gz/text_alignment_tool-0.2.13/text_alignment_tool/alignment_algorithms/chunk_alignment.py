# TODO: update for real support of new TextChunk data structure

import edlib
from text_alignment_tool.alignment_algorithms import AlignmentAlgorithm
from text_alignment_tool.shared_classes import (
    TextChunk,
    LetterList,
    TextAlignments,
    AlignmentKey,
)
from statistics import mean
from fuzzywuzzy import fuzz
import swalign


class ChunkAlignmentAlgorithm(AlignmentAlgorithm):
    """Aligns two texts based upon the chunking of the texts.
    It aims to match corresponding corresponding lines based
    upon greatest similarity, without making any deletions
    from the target text.
    """

    def __init__(self):
        super().__init__()

    def align(self) -> TextAlignments:
        if self._alignment.alignments:
            return self._alignment

        linewise_matches = comprehensive_linewise_matching(
            self._query,
            self._target,
            self._input_query_text_chunk_indices,
            self._input_target_text_chunk_indices,
        )

        # Find best matches for lines
        alignment = TextAlignments()
        linewise_dict: dict[int, list[int]] = {}
        for linewise_match in linewise_matches:
            if linewise_match[0] not in linewise_dict:
                linewise_dict[linewise_match[0]] = []
            linewise_dict[linewise_match[0]].append(linewise_match[1])

        # Calculate the actual corresponding chunks of the lines
        query_target_text_chunk_alignment: list[tuple[TextChunk, TextChunk]] = []
        for linewise_match_key in linewise_dict.keys():
            query_text_chunk_indices = self._input_query_text_chunk_indices[
                linewise_match_key
            ]
            if len(linewise_dict[linewise_match_key]) == 1:
                query_target_text_chunk_alignment.append(
                    (
                        query_text_chunk_indices,
                        self._input_target_text_chunk_indices[
                            linewise_dict[linewise_match_key][0]
                        ],
                    )
                )
                continue

            query_text = self._query[query_text_chunk_indices.indices]
            for target_line_index in sorted(
                linewise_dict[linewise_match_key],
                key=lambda k: self._input_target_text_chunk_indices[k].indices[-1]
                - self._input_target_text_chunk_indices[k].indices[0],
                reverse=True,
            ):
                target_text_chunk_indices = self._input_target_text_chunk_indices[
                    target_line_index
                ]
                target_text = self._target[target_text_chunk_indices.indices]
                (
                    target_start_idx,
                    target_end_idx,
                    query_start,
                    query_end,
                ) = perform_local_chunk_alignment(query_text, target_text)
                query_target_text_chunk_alignment.append(
                    (
                        TextChunk(
                            list(
                                range(
                                    query_text_chunk_indices.indices[0] + query_start,
                                    query_text_chunk_indices.indices[-1]
                                    + query_end
                                    + 1,
                                )
                            ),
                            query_text_chunk_indices.name,
                        ),
                        TextChunk(
                            list(
                                range(
                                    target_text_chunk_indices.indices[0] + query_start,
                                    target_text_chunk_indices.indices[-1]
                                    + query_end
                                    + 1,
                                )
                            ),
                            target_text_chunk_indices.name,
                        ),
                    )
                )
                # Nullify the matched sequence
                section_length = len(query_text[query_start : query_end + 1])
                query_text[query_start : query_end + 1] = [1] * section_length

        # Build also the full alignment (based upon the chunk alignment)
        for chunk_alignment in query_target_text_chunk_alignment:
            query = self._query[chunk_alignment[0].indices]
            target = self._target[chunk_alignment[1].indices]
            if query.size == 0 or target.size == 0:
                continue

            best_alignment = perform_global_alignment(
                query,
                target,
                chunk_alignment[0].indices[0],
                chunk_alignment[1].indices[0],
            )
            alignment.alignments = alignment.alignments + best_alignment

        # self.__query_target_text_chunk_alignment = query_target_text_chunk_alignment
        self._output_query_text_chunk_indices = [
            x[0] for x in query_target_text_chunk_alignment
        ]
        self._output_target_text_chunk_indices = [
            x[1] for x in query_target_text_chunk_alignment
        ]
        self._alignment = alignment
        return self._alignment


def comprehensive_linewise_matching(
    query_text: LetterList,
    target_text: LetterList,
    query_text_chunk_bounds: list[TextChunk],
    target_text_chunk_bounds: list[TextChunk],
) -> list[tuple[int, int]]:
    query_text_chunks = [
        "".join(chr(y) for y in query_text[x.indices]) for x in query_text_chunk_bounds
    ]
    mean_query_length = mean([len(x) for x in query_text_chunks])
    target_text_chunks = [
        "".join(chr(y) for y in target_text[x.indices])
        for x in target_text_chunk_bounds
    ]
    mean_target_length = mean([len(x) for x in target_text_chunks])

    scored_matches: list[tuple[int, int, int]] = []
    for target_index, target_text_chunk in enumerate(target_text_chunks):
        for query_index, query_text_chunk in enumerate(query_text_chunks):
            ratio = (
                fuzz.partial_ratio
                if len(query_text_chunk) < (mean_query_length / 2)
                and len(target_text_chunk) < (mean_target_length / 2)
                else fuzz.ratio
            )
            pair_distance = ratio(query_text_chunk, target_text_chunk)
            scored_matches.append((pair_distance, query_index, target_index))

    best_matches: list[tuple[int, int, int]] = []
    sorted_scored_matches = sorted(scored_matches, key=lambda x: x[0], reverse=True)
    remaining_matches: list[tuple[int, int, int]] = sorted_scored_matches.copy()
    for match in sorted_scored_matches:
        if match not in remaining_matches:
            continue

        best_matches.append(match)
        remaining_matches = list(
            filter(
                lambda x: x[1] != match[1] and x[2] != match[2],
                remaining_matches,
            )
        )

    return [(x[1], x[2]) for x in sorted(best_matches, key=lambda x: x[1])]


def perform_global_alignment(
    query_text: LetterList,
    target_text: LetterList,
    query_offset: int,
    target_offset: int,
) -> list[AlignmentKey]:
    alignments: list[AlignmentKey] = []
    query = "".join([chr(x) for x in query_text])
    target = "".join([chr(x) for x in target_text])

    result = edlib.align(query, target, task="path", mode="HW")
    nice = edlib.getNiceAlignment(result, query, target)
    query_count_idx = query_offset
    target_count_idx = target_offset + result["locations"][0][0]
    for idx in range(len(nice["query_aligned"])):
        alignments.append(AlignmentKey(query_count_idx, target_count_idx))
        if nice["query_aligned"][idx] != "-":
            query_count_idx += 1
        if nice["target_aligned"][idx] != "-":
            target_count_idx += 1

    return alignments


def perform_local_chunk_alignment(
    query_text: LetterList,
    target_text: LetterList,
) -> tuple[int, int, int, int]:
    # choose your own values here… 2 and -1 are common.
    match = 2
    mismatch = -1
    scoring = swalign.NucleotideScoringMatrix(match, mismatch)

    sw = swalign.LocalAlignment(scoring)  # you can also choose gap penalties, etc...
    target_transcription = "".join([chr(x) for x in target_text])
    query_transcription = "".join([chr(x) for x in query_text])
    alignment = sw.align(target_transcription, query_transcription)
    target_start_idx, target_end_idx, query_start, query_end = (
        alignment.r_pos,
        alignment.r_end,
        alignment.q_pos,
        alignment.q_end,
    )
    alignment.dump()

    return target_start_idx, target_end_idx, query_start, query_end
