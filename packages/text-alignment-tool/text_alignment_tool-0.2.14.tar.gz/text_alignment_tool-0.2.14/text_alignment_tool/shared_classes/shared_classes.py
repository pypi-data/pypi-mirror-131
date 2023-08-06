from dataclasses import dataclass
import numpy as np


LetterList = np.ndarray


@dataclass(init=True, frozen=True)
class TextChunk:
    __slots__ = ("indices", "name")
    indices: list[int]
    name: str


class AlignmentKey:
    def __init__(self, query_idx: int, target_idx: int):
        self.query_idx = query_idx
        self.target_idx = target_idx


class TextAlignments:
    def __init__(self):
        self.alignments: list[AlignmentKey] = []