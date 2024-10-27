# main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
from uuid import UUID

from app.repositories.note import NoteRepository
from app.repositories.user import UserProfileRepository 

from app.models.note import Note, NoteCreate, NoteUpdate
from app.models.user import UserProfile, UserProfileUpdate
from app.config import settings

app = FastAPI(
    title="Notes API",
    description="API for managing notes and user profiles",
    version="1.0.0"
)

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency injection
async def get_note_repo():
    return NoteRepository()

async def get_user_repo():
    return UserProfileRepository()

# Note endpoints
@app.post("/notes/", response_model=Note)
async def create_note(
    note: NoteCreate,
    note_repo: NoteRepository = Depends(get_note_repo)
):
    return await note_repo.create(note)

@app.get("/notes/{note_id}", response_model=Note)
async def get_note(
    note_id: int,
    note_repo: NoteRepository = Depends(get_note_repo)
):
    note = await note_repo.get(note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

# @app.get("/users/{user_id}/notes", response_model=List[Note])
@app.get("/users/{user_id}/notes")
def get_user_notes(
    # user_id: UUID,
    user_id: str,
    # page: int = 1,
    # page_size: int = 10,
    # note_repo: NoteRepository = Depends(get_note_repo)
):
    # return note_repo.get_user_notes(user_id, page, page_size)
    response = settings.supabase.table('notes')\
    .select("*")\
    .eq('user_id', user_id)\
    .order('created_at', desc=True)\
    .execute()

    return response.data

# @app.put("/notes/{note_id}", response_model=Note)
@app.put("/notes/{note_id}")
def update_note(
# async def update_note(
    note_id: int,
    # note: NoteUpdate,
    # note_repo: NoteRepository = Depends(get_note_repo)
):
    # Update the note in the Supabase table
    response = settings.supabase.table('notes')\
        .update(note_id)\
        .eq('id', note_id)\
            .execute()
    
    return response.data
        # .update(update_data)\
    # updated_note = await note_repo.update(note_id, note)

    # if not updated_note:
    #     raise HTTPException(status_code=404, detail="Note not found")
    # return updated_note

@app.delete("/notes/{note_id}")
async def delete_note(
    note_id: int,
    note_repo: NoteRepository = Depends(get_note_repo)
):
    success = await note_repo.delete(note_id)
    if not success:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": "Note deleted successfully"}

# User profile endpoints
@app.get("/users/{user_id}", response_model=UserProfile)
async def get_user_profile(
    user_id: UUID,
    user_repo: UserProfileRepository = Depends(get_user_repo)
):
    user = await user_repo.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users/username/{username}", response_model=UserProfile)
async def get_user_by_username(
    username: str,
    user_repo: UserProfileRepository = Depends(get_user_repo)
):
    user = await user_repo.get_by_username(username)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=UserProfile)
async def update_user_profile(
    user_id: UUID,
    profile: UserProfileUpdate,
    user_repo: UserProfileRepository = Depends(get_user_repo)
):
    updated_profile = await user_repo.update(user_id, profile)
    if not updated_profile:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_profile

@app.get("/users/search/{query}", response_model=List[UserProfile])
async def search_users(
    query: str,
    page: int = 1,
    page_size: int = 10,
    user_repo: UserProfileRepository = Depends(get_user_repo)
):
    return await user_repo.search(query, page, page_size)