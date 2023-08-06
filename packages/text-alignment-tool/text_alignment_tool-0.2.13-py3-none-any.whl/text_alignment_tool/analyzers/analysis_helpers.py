from typing import Sequence
from text_alignment_tool.shared_classes import LetterList, TextChunk, TextAlignments
from terminaltables import AsciiTable


def get_text_for_range(text: LetterList, start_idx: int, end_idx: int) -> str:
    return "".join([chr(x) for x in text[start_idx : end_idx + 1]])


def get_text_chunk_string(text: LetterList, chunk: TextChunk) -> str:
    return "".join([chr(x) for x in text[chunk.indices]])


def get_text_chunks_string(
    text: LetterList, chunks: Sequence[TextChunk], joiner: str = "\n"
) -> str:
    return joiner.join([get_text_chunk_string(text, x) for x in chunks])


def gather_query_parallels(
    query: LetterList, target: LetterList, alignments: TextAlignments
) -> list[tuple[str, str]]:
    query_map = {x.query_idx: x.target_idx for x in alignments.alignments}
    return [
        (chr(character), "")
        if idx not in query_map
        else (chr(character), chr(target[query_map[idx]]))
        for idx, character in enumerate(query)
    ]


def gather_target_parallels(
    query: LetterList, target: LetterList, alignments: TextAlignments
) -> list[tuple[str, str]]:
    target_map = {x.target_idx: x.query_idx for x in alignments.alignments}
    return [
        (chr(character), "")
        if idx not in target_map
        else (chr(character), chr(query[target_map[idx]]))
        for idx, character in enumerate(target)
    ]


def compare_parallel_text(
    query: LetterList, target: LetterList, alignments: TextAlignments
) -> list[str]:
    query_map = {x.query_idx: x.target_idx for x in alignments.alignments}
    target_map = {v: k for k, v in query_map.items()}
    response = ["Query → Target Alignment:"]
    response += [
        f"""{x[0]} → {x[1]}"""
        for x in gather_query_parallels(query, target, alignments)
    ]
    response += ["", "Target → Query Alignment:"]
    response += [
        f"""{x[0]} → {x[1]}"""
        for x in gather_target_parallels(query, target, alignments)
    ]
    return response


def compare_parallel_text_chunks(
    query: LetterList,
    query_chunks: Sequence[TextChunk],
    target: LetterList,
    target_chunks: Sequence[TextChunk],
    rtl=False,
) -> str:
    parallelized_text: list[list[str]] = [
        [
            get_text_chunk_string(query, x)[:: -1 if rtl else 1],
            get_text_chunk_string(target, y)[:: -1 if rtl else 1],
        ]
        for x, y in zip(query_chunks, target_chunks)
    ]
    parallelized_text.insert(0, ["query", "target"])
    table = AsciiTable(parallelized_text)
    table.inner_column_border = True
    table.justify_columns[0] = "center"
    table.justify_columns[1] = "center"
    return table.table


def print_parallel_text_chunks(
    query: LetterList,
    query_chunks: Sequence[TextChunk],
    target: LetterList,
    target_chunks: Sequence[TextChunk],
    rtl=False,
):
    comparison = compare_parallel_text_chunks(
        query, query_chunks, target, target_chunks, rtl
    )
    print(comparison)
