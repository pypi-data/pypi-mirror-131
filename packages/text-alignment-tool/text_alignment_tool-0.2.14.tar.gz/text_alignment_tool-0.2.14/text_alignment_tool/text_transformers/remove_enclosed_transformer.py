from typing import List
from text_alignment_tool.shared_classes import LetterList, TextChunk
from text_alignment_tool.text_transformers import TextTransformer
import numpy as np


class RemoveEnclosedTransformer(TextTransformer):
    def __init__(self, start_sign: str, end_sign: str):
        self.__start_sign = self.__verify_char_input(start_sign)
        self.__end_sign = self.__verify_char_input(end_sign)
        super().__init__()

    @staticmethod
    def __verify_char_input(char: str):
        if len(char) != 1:
            raise Exception(
                f"Must use only a single character not char: {char}, with length: {len(char)}"
            )
        return char

    def load_input(self, input: LetterList, text_chunk_indices: list[TextChunk]):
        super().load_input(input, text_chunk_indices, False)

    def transform(self) -> LetterList:
        if self._output.size > 0:
            return self._output

        self.__transform()

        return super().transform()

    def __transform(self):
        """Remove all characters betweek the start_sign and the end_sign.
        The start_sign and the end_sign should also be removed.
        """

        input_output_map: list[tuple[int, int]] = []
        start_code = ord(self.__start_sign)
        end_code = ord(self.__end_sign)
        delete_character_codes: list[int] = [start_code, end_code]

        output: list[int] = []
        output_chunks: list[TextChunk] = []
        remove_current = False
        for chunk in self._input_text_chunk_indices:
            current_chunk_indices: List[int] = []
            for idx in chunk.indices:
                char = self.input[idx]
                if char in delete_character_codes:
                    if char == start_code:
                        remove_current = True
                    if char == end_code:
                        remove_current = False
                    continue

                if remove_current:
                    continue

                output.append(char)
                current_char_index = len(output) - 1
                current_chunk_indices.append(current_char_index)
                input_output_map.append((idx, current_char_index))

            if current_chunk_indices:
                output_chunks.append(TextChunk(current_chunk_indices, chunk.name))

        self._input_output_map = input_output_map
        self._output = np.array(output, dtype=np.uint32)
        self._text_chunk_indices = output_chunks

    def __str__(self):
        return "\n".join(
            [
                "".join([chr(self._output[y]) for y in x.indices])
                for x in self._text_chunk_indices
            ]
        )
