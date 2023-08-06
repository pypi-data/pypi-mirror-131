from typing import Union, Any
from text_alignment_tool.shared_classes import (
    LetterList,
    TextChunk,
    TextAlignments,
    AlignmentKey,
)
from text_alignment_tool.analyzers import (
    compare_parallel_text_chunks,
    compare_parallel_text,
)
import numpy as np


class AlignmentException(Exception):
    pass


class AlignmentAlgorithm:
    """
    A class for performing a single text alignment operation.
    It may be used to redefine text chunks as well.
    """

    def __init__(self):
        pass

    def load_texts(
        self,
        query: LetterList,
        target: LetterList,
        input_query_text_chunk_indices: list[TextChunk],
        input_target_text_chunk_indices: list[TextChunk],
    ):
        self._query = query
        self._target = target
        self._input_query_text_chunk_indices = input_query_text_chunk_indices
        self._input_target_text_chunk_indices = input_target_text_chunk_indices
        self._output_query_text_chunk_indices: list[TextChunk] = []
        self._output_target_text_chunk_indices: list[TextChunk] = []
        self._alignment: TextAlignments = TextAlignments()

    def align(self) -> TextAlignments:
        if self._alignment.alignments:
            return self._alignment

        if self._query.size == 0:
            raise AlignmentException("The query text is empty")
        if self._target.size == 0:
            raise AlignmentException("The target text is empty")

        return TextAlignments()

    def apply_alignment(
        self, alignment_pairs: TextAlignments, aligned_text: LetterList
    ) -> Union[LetterList, Any]:
        input_to_aligned_text_map = TextAlignments()
        alignment_pairs_dict: dict[int, list[int]] = {}

        for alignment in alignment_pairs.alignments:
            if alignment.query_idx not in alignment_pairs_dict:
                alignment_pairs_dict[alignment.query_idx] = []

            alignment_pairs_dict[alignment.query_idx].append(alignment.target_idx)

        for input_idx, output_idx in [
            (x.query_idx, x.target_idx) for x in self.input_output_alignment.alignments
        ]:
            if output_idx in alignment_pairs_dict:
                for align_idx in alignment_pairs_dict[output_idx]:
                    input_to_aligned_text_map.alignments.append(
                        AlignmentKey(input_idx, align_idx)
                    )
                    pass

        input_to_aligned_text_map_dict: dict[int, list[int]] = {}
        for alignment in input_to_aligned_text_map.alignments:
            if alignment.query_idx not in alignment_pairs_dict:
                input_to_aligned_text_map_dict[alignment.query_idx] = []

            input_to_aligned_text_map_dict[alignment.query_idx].append(
                alignment.target_idx
            )

        input_with_alignment_applied = []
        for input_idx in range(self._query.size):
            if input_idx not in input_to_aligned_text_map_dict:
                input_with_alignment_applied.append(self._query[input_idx])
                continue

            for alignment_idx in input_to_aligned_text_map_dict[input_idx]:
                input_with_alignment_applied.append(aligned_text[alignment_idx])

        return np.array(input_with_alignment_applied)

    @property
    def chunked_query_text(self) -> list[tuple[str, str]]:
        """Retrieve a visualization of the current chunked query text

        Returns:
            list[tuple[str, str]]: A list containing the name and transcription of each text chunk
        """

        return [
            (y.name, "".join([chr(self._query[x]) for x in y.indices]))
            for y in self.output_query_text_chunk_indices
        ]

    @property
    def chunked_target_text(self) -> list[tuple[str, str]]:
        """Retrieve a visualization of the current chunked target text

        Returns:
            list[tuple[str, str]]: A list containing the name and transcription of each text chunk
        """

        return [
            (y.name, "".join([chr(self._target[x]) for x in y.indices]))
            for y in self.output_target_text_chunk_indices
        ]

    def aligned_chunked_text(self, rtl=False) -> str:
        """Visualize the alignment of the two texts by text chunk

        Args:
            rtl (bool, optional): Set the text direction to right-to-left. Defaults to False.

        Returns:
            str: A tabular representation of the text alignment
        """

        return compare_parallel_text_chunks(
            self._query,
            self.output_query_text_chunk_indices,
            self._target,
            self.output_target_text_chunk_indices,
            rtl,
        )

    def get_aligned_text(self) -> str:
        """Visualize the alignment of the two texts

        Returns:
            str: a string visualization of the aligned text
        """

        return "\n".join(
            compare_parallel_text(
                self._query,
                self._target,
                self._alignment,
            )
        )

    @property
    def input_output_alignment(self) -> TextAlignments:
        return self._alignment

    @property
    def input_query_text_chunk_indices(self) -> list[TextChunk]:
        if not self._input_query_text_chunk_indices:
            self._input_query_text_chunk_indices.append(
                TextChunk([x for x in range(0, self._query.size)], "default full text")
            )

        if self._input_query_text_chunk_indices:
            return self._input_query_text_chunk_indices

        raise AlignmentException(
            "No input query text chunk was created (this is a development error)"
        )

    @property
    def input_target_text_chunk_indices(self) -> list[TextChunk]:
        if not self._input_target_text_chunk_indices:
            self._input_target_text_chunk_indices.append(
                TextChunk([x for x in range(0, self._target.size)], "default full text")
            )

        if self._input_target_text_chunk_indices:
            return self._input_target_text_chunk_indices

        raise AlignmentException(
            "No input target text chunk was created (this is a development error)"
        )

    @property
    def output_query_text_chunk_indices(self) -> list[TextChunk]:
        if not self._output_query_text_chunk_indices:
            self._output_query_text_chunk_indices = self.input_query_text_chunk_indices

        return self._output_query_text_chunk_indices

    @property
    def output_target_text_chunk_indices(self) -> list[TextChunk]:
        if not self._output_target_text_chunk_indices:
            self._output_target_text_chunk_indices = (
                self.input_target_text_chunk_indices
            )

        return self._output_target_text_chunk_indices

    def __str__(self):
        query_to_target_alignment = {
            x.query_idx: chr(self._target[x.target_idx])
            for x in self._alignment.alignments
        }
        target_to_query_alignment = {
            x.target_idx: chr(self._query[x.query_idx])
            for x in self._alignment.alignments
        }
        return (
            "Query <-> Target\n"
            + "\n".join(
                [
                    chr(code)
                    + "<->"
                    + (
                        query_to_target_alignment[idx]
                        if idx in query_to_target_alignment
                        else ""
                    )
                    for idx, code in enumerate(self._query)
                ]
            )
            + "\nTarget <-> Query\n"
            + "\n".join(
                [
                    chr(code)
                    + "<->"
                    + (
                        target_to_query_alignment[idx]
                        if idx in target_to_query_alignment
                        else ""
                    )
                    for idx, code in enumerate(self._target)
                ]
            )
        )
