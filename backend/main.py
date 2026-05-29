from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os
import sys

# Append current directory to sys.path to allow relative imports
sys.path.append(os.path.dirname(__file__))

# Load env variables globally
load_dotenv()

from api.routes import router

app = FastAPI(title="WhatsApp Group Chat Analyzer API")

# Setup CORS for Frontend React integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the routes
app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    return {"message": "WhatsApp Group Chat Analyzer API is running."}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
