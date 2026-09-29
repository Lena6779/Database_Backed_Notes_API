from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class NoteCreate(BaseModel):
    title: str = Field(max_length=200)
    content: str
    category: str | None = Field(default=None, max_length=50)
    is_pinned: bool = False


class NoteResponse(NoteCreate):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)