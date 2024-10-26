
# app/repositories/user_repository.py
from typing import List, Optional
from datetime import datetime
from uuid import UUID
from .base import BaseRepository
from ..models.user import UserProfile, UserProfileUpdate

class UserProfileRepository(BaseRepository):
    def __init__(self):
        super().__init__()
        self.table = 'user_profiles'

    async def get(self, user_id: UUID) -> Optional[UserProfile]:
        response = await self.supabase.table(self.table)\
            .select("*")\
            .eq('id', str(user_id))\
            .single()\
            .execute()
        return UserProfile.model_validate(response.data) if response.data else None

    async def get_by_username(self, username: str) -> Optional[UserProfile]:
        response = await self.supabase.table(self.table)\
            .select("*")\
            .eq('username', username)\
            .single()\
            .execute()
        return UserProfile.model_validate(response.data) if response.data else None

    async def update(self, user_id: UUID, profile: UserProfileUpdate) -> Optional[UserProfile]:
        data = {
            **profile.model_dump(exclude_unset=True),
            'updated_at': datetime.now().isoformat()
        }
        response = await self.supabase.table(self.table)\
            .update(data)\
            .eq('id', str(user_id))\
            .execute()
        return UserProfile.model_validate(response.data[0]) if response.data else None

    async def search(
        self, 
        search_term: str, 
        page: int = 1, 
        page_size: int = None
    ) -> List[UserProfile]:
        query = self.supabase.table(self.table)\
            .select("*")\
            .or_(f"username.ilike.%{search_term}%,full_name.ilike.%{search_term}%")
            
        query = await self._paginate_query(query, page, page_size)
        response = await query.execute()
        
        return [UserProfile.model_validate(profile) for profile in response.data]