from __future__ import annotations

import re
from dataclasses import dataclass

from ..schemas.document import BBoxRegion, ParsedLine


@dataclass
class _CollapsedMap:
    collapsed: str
    char_map: list[int]


_WHITESPACE_RE = re.compile(r"\s")
_FRAGMENT_SPLIT_RE = re.compile(r"[，。；：,.!?；：\n\r\t]")


def _build_collapsed_map(text: str) -> _CollapsedMap:
    chars: list[str] = []
    char_map: list[int] = []
    for index, char in enumerate(text):
        if _WHITESPACE_RE.match(char):
            continue
        chars.append(char.lower())
        char_map.append(index)
    return _CollapsedMap(collapsed="".join(chars), char_map=char_map)


def _clean_snippet(snippet: str) -> str:
    return snippet.replace("\u2026", " ").replace("...", " ").strip()


def match_snippet_to_line_bboxes(
    page_number: int,
    page_lines: list[ParsedLine],
    snippet: str | None,
) -> list[BBoxRegion]:
    if not snippet or not page_lines:
        return []

    cleaned = _clean_snippet(snippet)
    if not cleaned:
        return []

    line_texts = [line.text for line in page_lines]
    line_offsets: list[int] = []
    combined_parts: list[str] = []
    cursor = 0
    for line_text in line_texts:
        line_offsets.append(cursor)
        combined_parts.append(line_text)
        cursor += len(line_text) + 1

    combined_text = "\n".join(combined_parts)

    source_map = _build_collapsed_map(combined_text)
    snippet_map = _build_collapsed_map(cleaned)
    if not snippet_map.collapsed or not source_map.collapsed:
        return []

    match_range = _locate_range(source_map, snippet_map.collapsed)
    if match_range is None:
        fragments = [
            fragment.strip()
            for fragment in _FRAGMENT_SPLIT_RE.split(cleaned)
            if len(fragment.strip()) >= 6
        ]
        fragments.sort(key=len, reverse=True)
        for fragment in fragments:
            fragment_map = _build_collapsed_map(fragment)
            match_range = _locate_range(source_map, fragment_map.collapsed)
            if match_range is not None:
                break

    if match_range is None:
        return []

    start_char, end_char = match_range
    covered = _lines_covering(start_char, end_char, line_offsets, line_texts)
    if not covered:
        return []

    return [
        BBoxRegion(
            page=page_number,
            x0=page_lines[index].bbox[0],
            y0=page_lines[index].bbox[1],
            x1=page_lines[index].bbox[2],
            y1=page_lines[index].bbox[3],
        )
        for index in covered
    ]


def _locate_range(source: _CollapsedMap, collapsed_snippet: str) -> tuple[int, int] | None:
    if not collapsed_snippet:
        return None
    index = source.collapsed.find(collapsed_snippet)
    if index == -1:
        return None
    start = source.char_map[index]
    end = source.char_map[index + len(collapsed_snippet) - 1] + 1
    return start, end


def _lines_covering(
    start_char: int,
    end_char: int,
    line_offsets: list[int],
    line_texts: list[str],
) -> list[int]:
    covered: list[int] = []
    for index, offset in enumerate(line_offsets):
        line_end = offset + len(line_texts[index])
        if line_end <= start_char:
            continue
        if offset >= end_char:
            break
        covered.append(index)
    return covered
