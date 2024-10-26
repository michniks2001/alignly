from supabase import create_client, Client
from ..config import settings

class BaseRepository:
    def __init__(self):
        self.supabase: Client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_KEY
        )
        self.table: str = None  # To be set by child classes

    async def _paginate_query(self, query, page: int = 1, page_size: int = None):
        if page_size is None:
            page_size = settings.DEFAULT_PAGE_SIZE
            
        page_size = min(page_size, settings.MAX_PAGE_SIZE)
        start = (page - 1) * page_size
        end = start + page_size - 1
        
        return query.range(start, end)