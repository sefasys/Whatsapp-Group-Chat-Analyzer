from fastapi import APIRouter, UploadFile, File, BackgroundTasks, HTTPException
import asyncio
from datetime import datetime

from utils.file_handler import save_upload_file, update_session_status, get_session_status, get_upload_path
from parser.chat_parser import parse_file
from parser.anonymizer import Anonymizer
from models.session import AnalysisSession, SessionStatus
from analyzer.pipeline import run as run_pipeline

router = APIRouter()

async def run_analysis_wrapper(session_id: str, provider: str = "gemini"):
    """Wrapper to prepare data, run pipeline, and periodically sync session status."""
    try:
        update_session_status(session_id, SessionStatus.PARSING.value, 5)
        file_path = get_upload_path(session_id)
        
        messages = parse_file(file_path)
        anonymizer = Anonymizer()
        messages = anonymizer.anonymize_messages(messages)
        
        # Create AnalysisSession for the pipeline
        session = AnalysisSession(session_id=session_id, created_at=datetime.now())
        
        # We need to sync session state with the disk periodically for the polling endpoint
        async def sync_session_state():
            while session.status not in (SessionStatus.COMPLETED, SessionStatus.FAILED):
                update_session_status(session_id, session.status.value, session.progress_pct)
                await asyncio.sleep(0.5)
                
        # Start the sync task
        sync_task = asyncio.create_task(sync_session_state())
        
        # Run the main pipeline from analyzer.pipeline
        report = await run_pipeline(session, messages, provider=provider)
        
        # Stop sync task and finalize
        sync_task.cancel()
        update_session_status(session_id, SessionStatus.COMPLETED.value, 100, report)
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        update_session_status(session_id, "failed", 0, {"error": str(e)})

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    """Accepts a WhatsApp .txt or .zip export and starts a session."""
    if not file.filename.endswith(('.txt', '.zip')):
        raise HTTPException(status_code=400, detail="Sadece .txt veya .zip dosyaları desteklenir")
        
    session_id = await save_upload_file(file)
    return {"session_id": session_id}

@router.post("/analyze/{session_id}")
async def start_analysis(session_id: str, background_tasks: BackgroundTasks, provider: str = "gemini"):
    """Starts the analysis pipeline asynchronously."""
    status = get_session_status(session_id)
    if status.get("status") == "not_found":
        raise HTTPException(status_code=404, detail="Session not found")
        
    background_tasks.add_task(run_analysis_wrapper, session_id, provider)
    return {"status": "started"}

@router.get("/report/{session_id}")
async def get_report(session_id: str):
    """Returns the current progress or final report of a session."""
    status = get_session_status(session_id)
    if status.get("status") == "not_found":
        raise HTTPException(status_code=404, detail="Session not found")
        
    return status
