import os
import json
import uuid
from typing import Dict, Any, Optional
import datetime
from fastapi import UploadFile

# Use absolute path based on project structure
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SESSIONS_DIR = os.path.join(BASE_DIR, "data", "sessions")
UPLOADS_DIR = os.path.join(BASE_DIR, "data", "uploads")

os.makedirs(SESSIONS_DIR, exist_ok=True)
os.makedirs(UPLOADS_DIR, exist_ok=True)

def _get_session_path(session_id: str) -> str:
    return os.path.join(SESSIONS_DIR, f"{session_id}.json")

def get_upload_path(session_id: str) -> str:
    return os.path.join(UPLOADS_DIR, f"{session_id}.txt")

import zipfile
import io

async def save_upload_file(upload_file: UploadFile) -> str:
    """Saves the uploaded file and returns a new session_id."""
    session_id = str(uuid.uuid4())
    content = await upload_file.read()
    
    # ZIP ise içinden .txt dosyasını çıkar
    if upload_file.filename.endswith(".zip"):
        with zipfile.ZipFile(io.BytesIO(content)) as z:
            txt_files = [f for f in z.namelist() if f.endswith(".txt")]
            if not txt_files:
                raise ValueError("ZIP içinde .txt dosyası bulunamadı")
            content = z.read(txt_files[0])
            
    file_path = get_upload_path(session_id)
    
    with open(file_path, "wb") as f:
        f.write(content)
        
    # Initialize session status
    update_session_status(session_id, "uploaded", 0, None)
    
    return session_id

def update_session_status(session_id: str, status: str, progress: int, result: Optional[Dict[str, Any]] = None):
    """Updates the status and progress of a session in a JSON file."""
    session_path = _get_session_path(session_id)
    
    data = {
        "session_id": session_id,
        "status": status,
        "progress": progress,
    }
    
    # If a result is passed, or if reading the existing file has a result, keep it
    if result is not None:
        data["result"] = result
    elif os.path.exists(session_path):
        try:
            with open(session_path, "r", encoding="utf-8") as f:
                existing = json.load(f)
                if "result" in existing:
                    data["result"] = existing["result"]
        except:
            pass
            
    def json_serializer(obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        raise TypeError(f"Type {type(obj)} not serializable")
        
    tmp_path = session_path + ".tmp"
    with open(tmp_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2, default=json_serializer)
    os.replace(tmp_path, session_path)

def get_session_status(session_id: str) -> Dict[str, Any]:
    """Reads the current session status."""
    session_path = _get_session_path(session_id)
    
    if not os.path.exists(session_path):
        return {"error": "Session not found", "status": "not_found", "progress": 0}
        
    try:
        with open(session_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        return {"error": f"JSON parsing error: {e}", "status": "error", "progress": 0}
