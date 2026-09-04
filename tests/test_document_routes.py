import pytest
from langchain_core.documents import Document

from app.routes.document_routes import (
    _get_section_metadata,
    _get_structural_query_target,
    _prepare_documents_sync,
)


# AI Genarated Code Start
@pytest.mark.parametrize(
    ("content", "current_index", "expected"),
    [
        ("第１２章 基本事項", None, (12, "基本事項", "第12章")),
        ("第十節 適用範囲", None, (10, "適用範囲", "第十節")),
        ("3.2 詳細設計", 2, (3, "詳細設計", "3.2")),
        ("一、概要", 3, (4, "概要", "一")),
        ("その1 補足", 4, (5, "補足", "その1")),
        ("A. 付録", 5, (6, "付録", "A")),
        ("IV. ローマ数字", 6, (7, "ローマ数字", "IV")),
        ("α. ギリシャ文字", 7, (7, None, None)),
        ("# A. Markdown appendix", None, (1, "Markdown appendix", "A")),
        ("## 通常の見出し", 8, (9, "通常の見出し", None)),
        ("第3章", 9, (9, None, None)),
        ("通常の本文です。", 9, (9, None, None)),
    ],
)
def test_get_section_metadata_recognizes_supported_heading_formats(
    content, current_index, expected
):
    assert _get_section_metadata(content, current_index) == expected


def test_prepare_documents_sync_propagates_section_label(monkeypatch):
    class IdentitySplitter:
        def __init__(self, **kwargs):
            pass

        def split_documents(self, documents):
            return documents

    monkeypatch.setattr(
        "app.routes.document_routes.RecursiveCharacterTextSplitter", IdentitySplitter
    )
    documents = [
        Document(page_content="第十節 適用範囲", metadata={}),
        Document(page_content="節の本文", metadata={}),
    ]

    prepared = _prepare_documents_sync(documents, "file-1", "user-1", False)

    assert prepared[0].metadata["section_index"] == 10
    assert prepared[0].metadata["section_title"] == "適用範囲"
    assert prepared[0].metadata["section_label"] == "第十節"
    assert prepared[1].metadata["section_label"] == "第十節"


def test_prepare_documents_sync_normalizes_powerpoint_slide_number(monkeypatch):
    class IdentitySplitter:
        def __init__(self, **kwargs):
            pass

        def split_documents(self, documents):
            return documents

    monkeypatch.setattr(
        "app.routes.document_routes.RecursiveCharacterTextSplitter", IdentitySplitter
    )

    # AI Genarated Code Start
    prepared = _prepare_documents_sync(
        [
            Document(
                page_content="Seventh slide content",
                metadata={"source": "slides.pptx", "page_number": 7},
            )
        ],
        "file-1",
        "user-1",
        False,
    )

    assert prepared[0].metadata["source_type"] == "pptx"
    assert prepared[0].metadata["slide_index"] == 6
    assert prepared[0].metadata["slide_number"] == 7
    assert prepared[0].metadata["page_number"] == 7
    # End of AI


@pytest.mark.parametrize(
    ("query", "expected"),
    [
        ("7スライド目の内容", ("slide_number", 7)),
        ("スライド 7 の内容", ("slide_number", 7)),
        ("slide 7 content", ("slide_number", 7)),
        ("7ページ目の内容", ("page_number", 7)),
    ],
)
def test_get_structural_query_target_recognizes_page_and_slide_requests(
    query, expected
):
    # AI Genarated Code Start
    assert _get_structural_query_target(query) == expected
    # End of AI


@pytest.mark.parametrize(
    ("query", "expected"),
    [
        ("2シート目の内容を取得して", ("sheet_number", 2)),
        ("第3シートの内容", ("sheet_number", 3)),
        ("シート 4 の内容", ("sheet_number", 4)),
        ("sheet 5 content", ("sheet_number", 5)),
        ("売上実績シートの内容", ("sheet_name", "売上実績")),
        ('シート「非表示」の内容', ("sheet_name", "非表示")),
        ('sheet "Sales" content', ("sheet_name", "Sales")),
    ],
)
def test_get_structural_query_target_recognizes_sheet_requests(query, expected):
    # AI Genarated Code Start
    assert _get_structural_query_target(query) == expected
    # End of AI
# End of AI