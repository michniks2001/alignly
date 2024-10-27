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
import os
import dotenv
import firebase_admin
from firebase_admin import credentials, auth, firestore
from datetime import datetime

from app.agent.get_events_from_data import agent_executor as event_agent_executor
from app.agent.get_events_from_data import output_agent_results


dotenv.load_dotenv()

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

cred_dict = {
    "type": "service_account",
    "project_id": "alignly-98902",
    "private_key_id": os.getenv("FIREBASE_PRIVATE_KEY_ID"),
    "private_key": os.getenv("FIREBASE_PRIVATE_KEY").replace('\\n', '\n'),
    "client_email": os.getenv("FIREBASE_CLIENT_EMAIL"),
    "client_id": os.getenv("FIREBASE_CLIENT_ID"),
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": os.getenv("FIREBASE_CLIENT_X509_CERT_URL")
}

cred = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(cred)
db = firestore.client()

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


@app.get("/users/{user_id}/notes", response_model=List[Note])
async def get_user_notes(
    user_id: UUID,
    page: int = 1,
    page_size: int = 10,
    note_repo: NoteRepository = Depends(get_note_repo)
):
    return await note_repo.get_user_notes(user_id, page, page_size)


@app.put("/notes/edit/{note_id}", response_model=Note)
async def update_note(
    note_id: int,
    # note: NoteUpdate,
    # note_repo: NoteRepository = Depends(get_note_repo)
):
    updated_note = await note_repo.update(note_id, note)
    if not updated_note:
        raise HTTPException(status_code=404, detail="Note not found")
    return updated_note


@app.delete("/notes/delete/{note_id}")
async def delete_note(
    note_id: int,
    note_repo: NoteRepository = Depends(get_note_repo)
):
    success = await note_repo.delete(note_id)
    if not success:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": "Note deleted successfully"}

# User profile endpoints


@app.get("/users/{user_id}")
async def get_user_profile_by_uuid(user_id: str):
    try:
        user = auth.get_user(user_id)
        return {
            'uuid': user.uid,
            'email': user.email
        }
    except auth.UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users/username/{email}")
async def get_user_by_email(email: str):
    try:
        user = auth.get_user_by_email(email)
        return {
            'uuid': user.uid,
            'email': user.email
        }
    except auth.UserNotFoundError:
        raise HTTPException(status_code=404, detail="User not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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


@app.get("/users/")
def list_all_users():
    try:
        users_list = []
        page = auth.list_users()
        
        for user in page.users:
            users_list.append({
                'uuid': user.uid,
                'email': user.email
            })
            
        return users_list
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
def get_next_note_id(user_id: str) -> int:
    # Get the user's notes collection
    notes_ref = db.collection(user_id).order_by('note_id', direction=firestore.Query.DESCENDING).limit(1)
    notes = notes_ref.get()
    
    # If there are no existing notes, start with 1
    if len(notes) == 0:
        return 1
    
    # Get the highest note_id and increment by 1
    return notes[0].to_dict()['note_id'] + 1

@app.post("/users/{user_id}/notes")
async def create_note(user_id: str, title: str, content: str):
    try:
        # Get the next note ID
        next_id = get_next_note_id(user_id)
        
        # Create the note document
        note = {
            'note_id': next_id,
            'title': title,
            'content': content,
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }
        
        # Add to user's collection using the auto-incremented ID
        doc_ref = db.collection(user_id).document(str(next_id))
        doc_ref.set(note)
        
        return {
            'user_id': user_id,
            'note_id': next_id,
            'message': 'Note created successfully'
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/users/{user_id}/notes")
async def get_user_notes(user_id: str):
    try:
        notes = []
        docs = db.collection(user_id).order_by('note_id').stream()
        
        for doc in docs:
            note_data = doc.to_dict()
            notes.append(note_data)
            
        return notes
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.put("/users/{user_id}/notes/{note_id}")
async def update_note(user_id: str, note_id: str, title: str, content: str):
    try:
        note_ref = db.collection(user_id).document(note_id)
        
        # Check if note exists
        if not note_ref.get().exists:
            raise HTTPException(status_code=404, detail="Note not found")
        
        # Update the note
        note_ref.update({
            'title': title,
            'content': content,
            'updated_at': datetime.now()
        })
        
        return {
            'user_id': user_id,
            'note_id': note_id,
            'message': 'Note updated successfully'
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/users/{user_id}/notes/{note_id}")
async def get_note_from_user(user_id: str, note_id: str):
    try:
        note_ref = db.collection(user_id).document(note_id)
        note = note_ref.get()
        
        if not note.exists:
            raise HTTPException(status_code=404, detail="Note not found")
            
        return note.to_dict()
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# Event Agent endpoints\
@app.get("/event_from_text/{user_id}/{note_id}")
async def get_event_from_text(user_id: str, note_id: str):
    try:
        note_ref = db.collection(user_id).document(note_id)
        note = note_ref.get()

        note_data = note.to_dict()

        text = note_data['content']

        results = output_agent_results(event_agent_executor, text)
        return results
        
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    # # Run the agent with the text
    # response = event_agent_executor.run(text)
    # return output_agent_results(response)