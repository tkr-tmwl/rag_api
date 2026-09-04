# app/models.py
import hashlib
from enum import Enum
from pydantic import BaseModel, Field
from typing import Optional, List


class DocumentResponse(BaseModel):
    page_content: str
    metadata: dict


class DocumentModel(BaseModel):
    page_content: str
    metadata: Optional[dict] = {}

    def generate_digest(self):
        hash_obj = hashlib.md5(self.page_content.encode())
        return hash_obj.hexdigest()


class StoreDocument(BaseModel):
    filepath: str
    filename: str
    file_content_type: str
    file_id: str


class QueryRequestBody(BaseModel):
    query: str
    file_id: str
    k: int = 4
    entity_id: Optional[str] = None
    # AI Genarated Code Start
    fallback_to_semantic: bool = True
    # End of AI


class CleanupMethod(str, Enum):
    incremental = "incremental"
    full = "full"


class QueryMultipleBody(BaseModel):
    query: str
    file_ids: List[str]
    k: int = 4


# AI Genarated Code Start
class DocumentContextRequest(BaseModel):
    """Request a deterministically selected page or section from one file."""

    file_id: str
    page_number: Optional[int] = Field(default=None, ge=1)
    # AI Genarated Code Start
    slide_number: Optional[int] = Field(default=None, ge=1)
    # End of AI
    section_index: Optional[int] = Field(default=None, ge=1)
    entity_id: Optional[str] = None

    def model_post_init(self, __context) -> None:
        # AI Genarated Code Start
        requested_scopes = sum(
            value is not None
            for value in (self.page_number, self.slide_number, self.section_index)
        )
        if requested_scopes != 1:
            raise ValueError(
                "Specify exactly one of page_number, slide_number, or section_index"
            )
        # End of AI
# End of AI
