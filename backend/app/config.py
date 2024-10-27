from dotenv import load_dotenv
import os
import supabase

load_dotenv()

class Settings:
    SUPABASE_URL: str = os.getenv('SUPABASE_URL')
    SUPABASE_KEY: str = os.getenv('SUPABASE_KEY')
    
    # Add any other configuration settings here
    DEFAULT_PAGE_SIZE: int = 10
    MAX_PAGE_SIZE: int = 100

    supabase = supabase.create_client(SUPABASE_URL, SUPABASE_KEY)

settings = Settings()