from __future__ import annotations

from scripts.extended_eval import EvalCase, EvalRecord, aggregate, score


def make_case(kind: str = "answerable") -> EvalCase:
    return EvalCase(
        case_id="doc:case",
        doc_id="doc",
        document_path="sample.md",
        language="zh",
        text="question",
        category="A1",
        kind=kind,
        expected_pages=[1],
        expected_any_of=["answer"],
        difficulty="easy",
    )


def test_extended_eval_classifies_model_refusal_after_retrieval() -> None:
    record = EvalRecord(
        case=make_case(),
        success=True,
        outcome="refused",
        retrieval_status="matched",
        evidence_mode="none",
        answer_snippet="无法从文档中找到相关依据回答此问题",
    )

    score(record)

    assert record.passed is False
    assert record.failure_type == "model_refused_after_retrieval"
    assert record.failure_stage == "model"


def test_extended_eval_classifies_wrong_page() -> None:
    record = EvalRecord(
        case=make_case(),
        success=True,
        outcome="answered",
        retrieval_status="matched",
        evidence_mode="declared",
        cited_pages=[2],
        citation_count=1,
        evidence_quote_count=1,
        answer_snippet="answer",
    )

    score(record)

    assert record.passed is False
    assert record.failure_type == "wrong_page"
    assert record.failure_stage == "citation"


def test_extended_eval_classifies_answer_missing_expected_term() -> None:
    record = EvalRecord(
        case=make_case(),
        success=True,
        outcome="answered",
        retrieval_status="matched",
        evidence_mode="declared",
        cited_pages=[1],
        citation_count=1,
        evidence_quote_count=1,
        answer_snippet="different text",
    )

    score(record)

    assert record.passed is False
    assert record.failure_type == "answer_missing_expected_term"
    assert record.failure_stage == "answer"


def test_extended_eval_aggregates_failure_types() -> None:
    failed = EvalRecord(
        case=make_case(),
        success=True,
        outcome="refused",
        retrieval_status="matched",
        evidence_mode="none",
        answer_snippet="无法回答",
    )
    passed = EvalRecord(
        case=make_case(),
        success=True,
        outcome="answered",
        retrieval_status="matched",
        evidence_mode="declared",
        cited_pages=[1],
        citation_count=1,
        evidence_quote_count=1,
        answer_snippet="answer",
    )
    score(failed)
    score(passed)

    summary = aggregate([failed, passed])

    assert summary["by_failure_type"] == {"model_refused_after_retrieval": 1}
    assert summary["by_failure_stage"] == {"model": 1}
