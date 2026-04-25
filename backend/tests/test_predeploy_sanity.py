from __future__ import annotations

from scripts.predeploy_sanity import CaseResult, GateCheck, render_report


def make_case(case_id: str, *, passed: bool = True) -> CaseResult:
    return CaseResult(
        case_id=case_id,
        kind="answerable",
        passed=passed,
        outcome="answered",
        retrieval_status="matched",
        evidence_mode="declared",
        cited_pages=[1],
        latency_ms=120,
        answer_snippet="ok",
        error=None,
        reason="" if passed else "missing citation",
    )


def test_predeploy_report_is_ready_only_when_cases_and_gates_pass() -> None:
    report = render_report(
        [make_case("a"), make_case("b")],
        [GateCheck("runtime_config", True, "ok"), GateCheck("pdf_page_render", True, "ok")],
        archive_path=None,
        timestamp="20260425_120000",
    )

    assert "**Status:** READY" in report
    assert "Gold cases: `2/2` passed" in report
    assert "Risk checks: `2/2` passed" in report


def test_predeploy_report_blocks_on_failed_gate() -> None:
    report = render_report(
        [make_case("a"), make_case("b")],
        [GateCheck("runtime_config", True, "ok"), GateCheck("pdf_page_render", False, "boom")],
        archive_path=None,
        timestamp="20260425_120000",
    )

    assert "**Status:** BLOCKED" in report
    assert "| pdf_page_render | FAIL | boom |" in report


def test_predeploy_report_blocks_on_failed_case() -> None:
    report = render_report(
        [make_case("a"), make_case("b", passed=False)],
        [GateCheck("runtime_config", True, "ok")],
        archive_path=None,
        timestamp="20260425_120000",
    )

    assert "**Status:** BLOCKED" in report
    assert "| b | answerable | FAIL | answered | matched | declared | [1] | 120 | missing citation |" in report
