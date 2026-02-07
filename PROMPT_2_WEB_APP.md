# Prompt 2: Claude Skills Web Interface

I need you to build a modern web application for interacting with Claude Skills through a chat interface.

## Overview

Create a FastAPI backend with a vanilla HTML/CSS/JavaScript frontend that allows users to:
- Chat with Claude using any available skill
- Upload and attach files to messages
- Adjust hyperparameters (temperature, max tokens)
- Export chat history to markdown
- Configure their own API key via a settings modal

## Architecture

### Backend: FastAPI (Python)

**File:** `web_app/app.py`

**Features:**
- Serve static HTML/CSS/JS files
- Accept API key from request headers (NOT from .env)
- List available skills
- Handle chat messages with optional skill selection
- File upload support
- Session management
- Export chat to markdown

**Key Endpoints:**

1. `GET /` - Serve index.html
2. `GET /api/skills` - List skills (requires `X-API-Key` header)
3. `POST /api/chat` - Send message (requires `X-API-Key` header)
4. `POST /api/upload` - Upload file
5. `GET /api/export/{session_id}` - Export chat as markdown

**API Integration:**
```python
from fastapi import FastAPI, Header, HTTPException
import anthropic

@app.get("/api/skills")
async def list_skills(x_api_key: str = Header(None, alias="X-API-Key")):
    if not x_api_key:
        raise HTTPException(status_code=401, detail="API key required")
    
    user_client = anthropic.Anthropic(api_key=x_api_key)
    skills_response = user_client.beta.skills.list(betas=["skills-2025-10-02"])
    # ... return formatted skills

@app.post("/api/chat")
async def chat(request: ChatRequest, x_api_key: str = Header(None, alias="X-API-Key")):
    if not x_api_key:
        raise HTTPException(status_code=401, detail="API key required")
    
    user_client = anthropic.Anthropic(api_key=x_api_key)
    
    # Build messages from session history
    # Add skill if specified:
    api_params = {
        "model": "claude-opus-4-6",
        "max_tokens": request.max_tokens,
        "temperature": request.temperature,
        "messages": api_messages
    }
    
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
    
    response = user_client.beta.messages.create(**api_params)
    # ... return response
```

**Dependencies (requirements.txt):**
```
fastapi==0.115.6
uvicorn[standard]==0.34.0
anthropic==0.78.0
python-dotenv==1.0.1
python-multipart==0.0.20
```

### Frontend: HTML/CSS/JavaScript

**File Structure:**
```
web_app/
├── app.py
├── requirements.txt
├── static/
│   ├── index.html
│   ├── style.css
│   └── app.js
└── uploads/
```

## Frontend Specifications

### HTML (`static/index.html`)

**Layout:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Claude Skills Interface</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <div class="container">
        <!-- Header with title and buttons -->
        <header class="header">
            <h1>🤖 Claude Skills Interface</h1>
            <div class="header-controls">
                <button id="settingsBtn">⚙️ Settings</button>
                <button id="exportBtn">📥 Export Chat</button>
                <button id="clearBtn">🗑️ Clear</button>
            </div>
        </header>

        <div class="main-content">
            <!-- Sidebar with controls -->
            <aside class="sidebar">
                <div class="control-group">
                    <label>Select Skill</label>
                    <select id="skillSelect">
                        <option value="">No Skill (Standard Claude)</option>
                    </select>
                </div>

                <div class="control-group">
                    <label>Temperature: <span id="tempValue">1.0</span></label>
                    <input type="range" id="temperature" min="0" max="2" step="0.1" value="1.0">
                </div>

                <div class="control-group">
                    <label>Max Tokens</label>
                    <input type="number" id="maxTokens" value="4096">
                </div>

                <div class="stats">
                    <h3>Session Stats</h3>
                    <div class="stat-item">
                        <span>Messages:</span>
                        <span id="messageCount">0</span>
                    </div>
                    <div class="stat-item">
                        <span>Tokens:</span>
                        <span id="tokenCount">0</span>
                    </div>
                </div>
            </aside>

            <!-- Chat area -->
            <div class="chat-container">
                <div id="chatMessages" class="chat-messages">
                    <div class="welcome-message">
                        <h2>👋 Welcome to Claude Skills</h2>
                        <p>Select a skill from the sidebar and start chatting!</p>
                    </div>
                </div>

                <!-- Input area -->
                <div class="input-container">
                    <div id="attachmentPreview" class="attachment-preview"></div>
                    <div class="input-wrapper">
                        <button id="attachBtn" class="btn-icon">📎</button>
                        <textarea id="messageInput" placeholder="Type your message..."></textarea>
                        <button id="sendBtn" class="btn-primary">Send</button>
                    </div>
                    <input type="file" id="fileInput" multiple hidden>
                </div>
            </div>
        </div>
    </div>

    <!-- Settings Modal -->
    <div id="settingsModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h2>⚙️ Settings</h2>
                <button class="modal-close" onclick="closeSettings()">✕</button>
            </div>
            <div class="modal-body">
                <div class="control-group">
                    <label>Anthropic API Key *</label>
                    <input type="password" id="apiKeyInput" placeholder="sk-ant-...">
                    <small>Your API key is stored locally in your browser.</small>
                </div>
                <div class="control-group">
                    <label>Default Skill ID (optional)</label>
                    <input type="text" id="defaultSkillInput" placeholder="skill_01...">
                </div>
                <div id="settingsStatus" class="settings-status"></div>
            </div>
            <div class="modal-footer">
                <button onclick="closeSettings()">Cancel</button>
                <button onclick="saveSettings()">Save Settings</button>
            </div>
        </div>
    </div>

    <script src="/static/app.js"></script>
</body>
</html>
```

### CSS (`static/style.css`)

**Design Requirements:**
- **Dark mode theme** with deep blues/purples
- **Glassmorphism effects** on panels (backdrop-filter: blur)
- **Smooth animations** for messages, modals
- **Modern controls** with hover effects
- **Responsive layout** (hide sidebar on mobile)

**Color Scheme:**
```css
:root {
    --bg-primary: #0f0f23;
    --bg-secondary: #1a1a2e;
    --bg-tertiary: #16213e;
    --accent: #6c63ff;
    --accent-hover: #5a52d5;
    --text-primary: #e4e4e7;
    --text-secondary: #a1a1aa;
    --border: rgba(255, 255, 255, 0.1);
    --user-msg: #2563eb;
    --assistant-msg: rgba(255, 255, 255, 0.05);
}
```

**Key Styles:**
- Glassmorphism: `background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px);`
- Message bubbles with rounded corners
- Typing indicator with animated dots
- Modal with slide-in animation
- Custom scrollbar styling

### JavaScript (`static/app.js`)

**Core Functionality:**

1. **Settings Management (localStorage):**
```javascript
function loadSettingsFromStorage() {
    const apiKey = localStorage.getItem('anthropic_api_key');
    const defaultSkill = localStorage.getItem('default_skill_id');
    // Load into inputs
}

function saveSettings() {
    const apiKey = apiKeyInput.value.trim();
    if (!apiKey.startsWith('sk-ant-')) {
        showError('Invalid API key format');
        return;
    }
    localStorage.setItem('anthropic_api_key', apiKey);
    localStorage.setItem('default_skill_id', defaultSkillInput.value.trim());
    loadSkills(); // Reload with new key
}

function getApiKey() {
    return localStorage.getItem('anthropic_api_key');
}
```

2. **Load Skills:**
```javascript
async function loadSkills() {
    const apiKey = getApiKey();
    if (!apiKey) return;
    
    const response = await fetch('/api/skills', {
        headers: { 'X-API-Key': apiKey }
    });
    const data = await response.json();
    
    // Populate skillSelect dropdown
    // Set default skill if configured
}
```

3. **Send Message:**
```javascript
async function sendMessage() {
    const apiKey = getApiKey();
    if (!apiKey) {
        openSettings();
        return;
    }
    
    const message = messageInput.value.trim();
    if (!message) return;
    
    // Add user message to chat
    addMessage('user', message);
    
    // Show typing indicator
    const typingId = showTypingIndicator();
    
    const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-API-Key': apiKey
        },
        body: JSON.stringify({
            message: message,
            skill_id: skillSelect.value || null,
            session_id: sessionId,
            temperature: parseFloat(temperature.value),
            max_tokens: parseInt(maxTokens.value),
            attachments: attachedFiles
        })
    });
    
    const data = await response.json();
    
    // Remove typing indicator
    removeTypingIndicator(typingId);
    
    // Add assistant response
    addMessage('assistant', data.response);
    
    // Update stats
    updateStats(data.usage);
}
```

4. **UI Functions:**
- `addMessage(role, content)` - Add message bubble to chat
- `showTypingIndicator()` - Show animated typing dots
- `exportChat()` - Download chat as markdown
- `clearChat()` - Reset session
- `openSettings()` / `closeSettings()` - Modal controls

**Session Management:**
- Generate unique session ID on load: `'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9)`
- Track messages, tokens in global state
- Persist session history on backend

## Startup & Testing

**Run the app:**
```bash
cd web_app
python app.py
```

**Test checklist:**
1. Settings modal opens on first load (no API key)
2. Can save API key and it persists in localStorage
3. Skills load after API key is saved
4. Can select a skill from dropdown
5. Can send messages and receive responses
6. Temperature and max tokens controls work
7. Can attach files
8. Export chat creates markdown file
9. Clear chat resets session
10. Stats update correctly

## Security Notes

- API keys stored ONLY in browser localStorage
- API keys sent in `X-API-Key` header to backend
- Backend creates new Anthropic client per request with user's key
- Server never stores or logs API keys

## Design Goals

- **Beautiful:** Modern dark mode with glassmorphism
- **Intuitive:** Clear controls, helpful error messages
- **Secure:** Client-side API key storage
- **Fast:** Minimal dependencies, vanilla JS
- **Responsive:** Works on desktop and mobile

Build this as a complete, production-ready web application that anyone can run locally to interact with their Claude Skills!
