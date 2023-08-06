from typing import List
from typing import TypeVar
from dataclasses import dataclass
import numpy as np
import numpy.typing as npt


LetterList = npt.NDArray[np.uint32]


@dataclass(init=True, frozen=True)
class TextChunk:
    __slots__ = ("indices", "name")
    indices: List[int]
    name: str


class AlignmentKey:
    def __init__(self, query_idx: int, target_idx: int):
        self.query_idx = query_idx
        self.target_idx = target_idx


class TextAlignments:
    def __init__(self):
        self.alignments: List[AlignmentKey] = []
