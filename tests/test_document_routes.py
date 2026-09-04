import pytest
from langchain_core.documents import Document

from app.routes.document_routes import _get_section_metadata, _prepare_documents_sync


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
        ("α. ギリシャ文字", 7, (8, "ギリシャ文字", "α")),
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
# End of AI