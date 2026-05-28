"""API endpoint definitions.
POST /upload       → Upload and parse the chat file
POST /analyze      → Start the analysis process
GET  /report/{id}  → Fetch the analysis report
GET  /users/{id}   → Fetch group users list
"""
from fastapi import APIRouter, UploadFile, File
from fastapi.responses import JSONResponse

router = APIRouter()

@router.post("/upload")
async def upload_chat(file: UploadFile = File(...)):
    # 1. Read file (.txt or .zip)
    # 2. Call parser.chat_parser.parse()
    # 3. Return normalized data
    pass

@router.post("/analyze/{session_id}")
async def analyze_chat(session_id: str):
    # 1. Load parsed data
    # 2. Call analyzer.pipeline.run()
    # 3. Trigger async analysis job
    pass

@router.get("/report/{session_id}")
async def get_report(session_id: str):
    # Return completed analysis report
    pass

@router.get("/users/{session_id}")
async def get_users(session_id: str):
    # Return list of all users in the group
    pass

@router.get("/user/{session_id}/{user_id}")
async def get_user_profile(session_id: str, user_id: str):
    # Return single user profile + psychological analysis
    pass
