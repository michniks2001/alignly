from app.repositories.note_repository import NoteRepository
from app.repositories.user_repository import UserProfileRepository
from app.models.note import NoteCreate
from uuid import UUID

async def main():
    # Initialize repositories
    note_repo = NoteRepository()
    user_repo = UserProfileRepository()
    
    # Create a note
    new_note = NoteCreate(
        title="Test Note",
        content="This is a test note",
        user_id=UUID('dd36bf87-4d40-4f3d-a631-e6d98b425321')
    )
    note = await note_repo.create(new_note)
    
    # Get user profile
    user = await user_repo.get(UUID('dd36bf87-4d40-4f3d-a631-e6d98b425321'))
    
    # Get user's notes with pagination
    notes = await note_repo.get_user_notes(user.id, page=1, page_size=10)