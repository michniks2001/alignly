# main.py
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import os
import dotenv
import firebase_admin
from firebase_admin import credentials, auth, firestore
from datetime import datetime
import logging
import traceback

from app.agent.get_events_from_data import agent_executor as event_agent_executor
from app.agent.get_events_from_data import output_agent_results

from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    password: str


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


# Note endpoints


# User profile endpoints

@app.post("/users/create")
async def create_user(user: UserCreate):
    try:
        # Create the user in Firebase Auth
        user_record = auth.create_user(
            email=user.email,
            password=user.password
        )
        
        return {
            'uuid': user_record.uid,
            'email': user_record.email
        }
        
    except auth.EmailAlreadyExistsError:
        raise HTTPException(status_code=400, detail="Email already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


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

@app.get("/users/get_user_from_email/{email}")
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

@app.post("/users/{user_id}/create_notes")
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

logging.basicConfig(level=logging.INFO)

class NoteUpdate(BaseModel):
    title: str
    content: str
    
@app.put("/users/{user_id}/update_notes/{note_id}")
async def update_note(user_id: str, note_id: str, note: NoteUpdate):
    try:
        note_ref = db.collection(user_id).document(note_id)
        
        # Check if note exists
        if not note_ref.get().exists:
            raise HTTPException(status_code=404, detail="Note not found")
        
        # Update the note
        note_ref.update({
            'title': note.title,
            'content': note.content,
            'updated_at': datetime.now()
        })
        
        return {
            'user_id': user_id,
            'note_id': note_id,
            'message': 'Note updated successfully'
        }
        
    except Exception as e:
        logging.error("Error occured: %s", str(e))
        logging.debug("Traceback: %s", traceback.format_exc())
        raise HTTPException(status_code=500, detail=str(e))
    

@app.get("/users/{user_id}/get_notes/{note_id}")
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

# Utility function to get the next event ID
def get_next_event_id(user_id: str) -> int:
    events_ref = db.collection(f"{user_id}_events").order_by('event_id', direction=firestore.Query.DESCENDING).limit(1)
    events = events_ref.get()
    
    # If there are no existing events, start with 1
    if len(events) == 0:
        return 1
    
    # Get the highest event_id and increment by 1
    return events[0].to_dict()['event_id'] + 1

# Endpoint to create an event based on a note's content
@app.post("/users/{user_id}/create_event_from_note/{note_id}")
async def create_event_from_note(user_id: str, note_id: str):
    
    try:
        # Fetch the note
        note_ref = db.collection(user_id).document(note_id)
        note = note_ref.get()
        
        if not note.exists:
            raise HTTPException(status_code=404, detail="Note not found")
        
        note_data = note.to_dict()
        text = note_data['content']

        # Use the event agent to extract event information from the note's content
        results = output_agent_results(event_agent_executor, text)

        # Get the next event ID
        next_event_id = get_next_event_id(user_id)
        
        # Structure the event data
        event = {
            'event_id': next_event_id,
            'note_id': note_id,
            'content': results,
            'created_at': datetime.now(),
            'updated_at': datetime.now()
        }

        # Add the event to the user's event collection
        doc_ref = db.collection(f"{user_id}_events").document(str(next_event_id))
        doc_ref.set(event)
        
        return {
            'user_id': user_id,
            'event_id': next_event_id,
            'message': 'Event created successfully'
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to get all events for a user
@app.get("/users/{user_id}/events")
async def get_user_events(user_id: str):
    try:
        events = []
        docs = db.collection(f"{user_id}_events").order_by('event_id').stream()
        
        for doc in docs:
            event_data = doc.to_dict()
            events.append(event_data)
            
        return events
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Endpoint to get a specific event by ID
@app.get("/users/{user_id}/get_event/{event_id}")
async def get_event(user_id: str, event_id: str):
    try:
        event_ref = db.collection(f"{user_id}_events").document(event_id)
        event = event_ref.get()
        
        if not event.exists:
            raise HTTPException(status_code=404, detail="Event not found")
            
        return event.to_dict()
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))