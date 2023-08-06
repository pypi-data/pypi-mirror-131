from typing import List
from text_alignment_tool.shared_classes import TextChunk, LetterList
from text_alignment_tool.text_loaders.text_loader import TextLoader
import numpy as np
import re


class NewlineSeparatedTextLoader(TextLoader):
    def __init__(self, input_text: str):
        super().__init__()
        self.__input_text = input_text

    def _load(self) -> LetterList:
        self._output = np.array(
            [ord(" ") if x == "\n" else ord(x) for x in self.__input_text]
        )

        text_chunks: List[TextChunk] = []
        start_chunk_idx = 0
        chunk_count = 0
        for chunk_match in self.__input_text.split("\n"):
            chunk_length = len(chunk_match)
            text_chunks.append(
                TextChunk(
                    list(range(start_chunk_idx, start_chunk_idx + chunk_length)),
                    f"line {chunk_count}",
                )
            )
            chunk_count += 1
            start_chunk_idx += chunk_length
        self._input_output_map = [(x, x) for x in range(0, self.output.size)]
        self._text_chunk_indices = text_chunks

        return super()._load()
