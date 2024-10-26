# app/models/note.py
from datetime import datetime
from typing import Optional
from uuid import UUID
from pydantic import BaseModel

class NoteBase(BaseModel):
    title: str
    content: str

class NoteCreate(NoteBase):
    user_id: UUID

class NoteUpdate(NoteBase):
    pass

class Note(NoteBase):
    id: int
    user_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
