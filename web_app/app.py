"""
FastAPI backend for Claude Skills web interface.
Provides endpoints for chat, file uploads, and skill management.
"""

import os
import json
import base64
from datetime import datetime
from typing import Optional, List
from pathlib import Path

from fastapi import FastAPI, UploadFile, File, Form, HTTPException, Header
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
import anthropic

# Load environment variables
load_dotenv()

app = FastAPI(title="Claude Skills Interface")

# Enable CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

# In-memory session storage (for demo purposes)
sessions = {}

# Models
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    message: str
    skill_id: Optional[str] = None
    session_id: str
    temperature: float = 1.0
    max_tokens: int = 4096
    attachments: Optional[List[dict]] = None

class SkillInfo(BaseModel):
    id: str
    name: str
    type: str
    description: Optional[str] = None

# Routes
@app.get("/")
async def root():
    """Serve the main HTML page"""
    return FileResponse("static/index.html")

@app.get("/api/skills")
async def list_skills(x_api_key: str = Header(None, alias="X-API-Key")):
    """List all available Claude Skills"""
    if not x_api_key:
        raise HTTPException(status_code=401, detail="API key required")
    
    try:
        # Create client with user's API key
        user_client = anthropic.Anthropic(api_key=x_api_key)
        skills_response = user_client.beta.skills.list(betas=["skills-2025-10-02"])
        
        skills = []
        for skill in skills_response.data:
            skills.append({
                "id": skill.id,
                "name": skill.display_title,
                "type": skill.source,
                "description": getattr(skill, 'description', None)
            })
        
        return {"skills": skills}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    """Handle file uploads"""
    try:
        # Create uploads directory if it doesn't exist
        upload_dir = Path("uploads")
        upload_dir.mkdir(exist_ok=True)
        
        # Save file
        file_path = upload_dir / file.filename
        content = await file.read()
        
        with open(file_path, "wb") as f:
            f.write(content)
        
        # Read file content for text files
        file_content = None
        if file.content_type and file.content_type.startswith("text"):
            file_content = content.decode("utf-8")
        
        return {
            "filename": file.filename,
            "size": len(content),
            "type": file.content_type,
            "content": file_content,
            "path": str(file_path)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/chat")
async def chat(request: ChatRequest, x_api_key: str = Header(None, alias="X-API-Key")):
    """Send message to Claude with optional skill"""
    if not x_api_key:
        raise HTTPException(status_code=401, detail="API key required")
    
    try:
        # Create client with user's API key
        user_client = anthropic.Anthropic(api_key=x_api_key)
        
        # Get or create session
        if request.session_id not in sessions:
            sessions[request.session_id] = []
        
        # Add user message to session
        sessions[request.session_id].append({
            "role": "user",
            "content": request.message,
            "timestamp": datetime.now().isoformat()
        })
        
        # Prepare messages for API
        api_messages = []
        for msg in sessions[request.session_id]:
            api_messages.append({
                "role": msg["role"],
                "content": msg["content"]
            })
        
        # Prepare API request parameters
        api_params = {
            "model": "claude-opus-4-6",
            "max_tokens": request.max_tokens,
            "temperature": request.temperature,
            "messages": api_messages
        }
        
        # Add skill if specified
        if request.skill_id:
            skill_type = "custom" if request.skill_id.startswith("skill_") else "anthropic"
            api_params["betas"] = ["code-execution-2025-08-25", "skills-2025-10-02"]
            api_params["container"] = {
                "skills": [{
                    "type": skill_type,
                    "skill_id": request.skill_id,
                    "version": "latest"
                }]
            }
            api_params["tools"] = [{"type": "code_execution_20250825", "name": "code_execution"}]
        
        # Call Claude API with user's key
        response = user_client.beta.messages.create(**api_params)
        
        # Extract response text
        response_text = ""
        for block in response.content:
            if hasattr(block, 'text'):
                response_text += block.text
        
        # Add assistant response to session
        sessions[request.session_id].append({
            "role": "assistant",
            "content": response_text,
            "timestamp": datetime.now().isoformat()
        })
        
        return {
            "response": response_text,
            "usage": {
                "input_tokens": response.usage.input_tokens,
                "output_tokens": response.usage.output_tokens
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/export/{session_id}")
async def export_chat(session_id: str):
    """Export chat history as markdown"""
    if session_id not in sessions:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Generate markdown
    markdown = f"# Claude Skills Chat Export\n\n"
    markdown += f"**Exported:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
    markdown += "---\n\n"
    
    for msg in sessions[session_id]:
        role = "**User**" if msg["role"] == "user" else "**Assistant**"
        timestamp = msg.get("timestamp", "")
        markdown += f"### {role}\n"
        if timestamp:
            markdown += f"*{timestamp}*\n\n"
        markdown += f"{msg['content']}\n\n"
        markdown += "---\n\n"
    
    # Save to file
    timestamp = datetime.now().strftime("%y.%m.%d.%H.%M.%S")
    filename = f"chat_export_{timestamp}.md"
    
    return JSONResponse({
        "markdown": markdown,
        "filename": filename
    })

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("WEB_APP_HOST", "127.0.0.1")
    port = int(os.getenv("WEB_APP_PORT", "8000"))
    uvicorn.run(app, host=host, port=port)
