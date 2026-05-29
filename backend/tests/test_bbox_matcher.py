from __future__ import annotations

from backend.app.schemas.document import ParsedLine
from backend.app.services.bbox_matcher import match_snippet_to_line_bboxes


def _line(text: str, bbox: tuple[float, float, float, float]) -> ParsedLine:
    return ParsedLine(text=text, bbox=bbox)


def test_exact_single_line_match_returns_that_line() -> None:
    lines = [
        _line("The first-phase goal is to support upload and ask.", (10, 20, 300, 32)),
        _line("Another unrelated sentence about background.", (10, 40, 300, 52)),
    ]
    regions = match_snippet_to_line_bboxes(3, lines, "first-phase goal is to support upload")
    assert len(regions) == 1
    assert regions[0].page == 3
    assert (regions[0].x0, regions[0].y0) == (10, 20)


def test_quote_spanning_two_lines_covers_both() -> None:
    lines = [
        _line("Attention is all you need and the", (10, 20, 300, 32)),
        _line("Transformer dispenses with recurrence.", (10, 40, 300, 52)),
    ]
    # the quote straddles the line break (lines are joined with "\n")
    regions = match_snippet_to_line_bboxes(1, lines, "the Transformer dispenses with recurrence")
    assert len(regions) == 2
    assert {region.y0 for region in regions} == {20, 40}


def test_whitespace_differences_still_match() -> None:
    # the model quote often differs from PDF line text only by collapsed spaces
    lines = [_line("模型 推理 在 云端 完成", (5, 5, 200, 18))]
    regions = match_snippet_to_line_bboxes(2, lines, "模型推理在云端完成")
    assert len(regions) == 1
    assert regions[0].y0 == 5


def test_fragment_fallback_when_full_snippet_not_contiguous() -> None:
    # full snippet is not a contiguous substring, but a >=6-char fragment is
    lines = [_line("总体准确率为 56.20%。", (10, 20, 300, 32))]
    regions = match_snippet_to_line_bboxes(4, lines, "作者最终方法排名第六，总体准确率为 56.20%")
    assert len(regions) == 1
    assert regions[0].y0 == 20


def test_no_match_returns_empty() -> None:
    lines = [_line("Completely different content.", (0, 0, 10, 10))]
    assert match_snippet_to_line_bboxes(1, lines, "an entirely nonexistent phrase") == []


def test_empty_inputs_return_empty() -> None:
    assert match_snippet_to_line_bboxes(1, [], "anything") == []
    assert match_snippet_to_line_bboxes(1, [_line("x", (0, 0, 1, 1))], "") == []
    assert match_snippet_to_line_bboxes(1, [_line("x", (0, 0, 1, 1))], None) == []
