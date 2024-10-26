# app/repositories/note_repository.py
from typing import List, Optional
from datetime import datetime
from uuid import UUID
from .base import BaseRepository
from ..models.note import Note, NoteCreate, NoteUpdate

class NoteRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.table = 'notes'

    async def create(self, note: NoteCreate) -> Note:
        data = {
            **note.model_dump(),
            'updated_at': datetime.now().isoformat()
        }
        response = await self.supabase.table(self.table).insert(data).execute()
        return Note.model_validate(response.data[0])

    async def get(self, note_id: int) -> Optional[Note]:
        response = await self.supabase.table(self.table)\
            .select("*")\
            .eq('id', note_id)\
            .single()\
            .execute()
        return Note.model_validate(response.data) if response.data else None

    async def get_user_notes(
        self, 
        user_id: UUID, 
        page: int = 1, 
        page_size: int = None
    ) -> List[Note]:
        query = self.supabase.table(self.table)\
            .select("*")\
            .eq('user_id', str(user_id))\
            .order('created_at', desc=True)
        
        query = await self._paginate_query(query, page, page_size)
        response = await query.execute()
        
        return [Note.model_validate(note) for note in response.data]

    async def update(self, note_id: int, note: NoteUpdate) -> Optional[Note]:
        data = {
            **note.model_dump(),
            'updated_at': datetime.now().isoformat()
        }
        response = await self.supabase.table(self.table)\
            .update(data)\
            .eq('id', note_id)\
            .execute()
        return Note.model_validate(response.data[0]) if response.data else None

    async def delete(self, note_id: int) -> bool:
        response = await self.supabase.table(self.table)\
            .delete()\
            .eq('id', note_id)\
            .execute()
        return bool(response.data)
