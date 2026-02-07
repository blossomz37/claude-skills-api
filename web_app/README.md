# Claude Skills Web Interface

A modern web application for interacting with Claude Skills through a beautiful chat interface.

## Features

- 💬 **Chat Interface** - Clean, modern chat UI with markdown support
- 📎 **File Attachments** - Upload and attach files to your messages
- 🎯 **Skill Selection** - Choose from your custom and pre-built skills
- ⚙️ **Hyperparameter Controls** - Adjust temperature and max tokens
- 📥 **Export to Markdown** - Download your entire chat history
- 🎨 **Modern UI** - Dark mode with glassmorphism effects
- 📊 **Session Stats** - Track messages and token usage

## Setup

### 1. Install Dependencies

```bash
cd web_app
pip install -r requirements.txt
```

Or using the system Python:

```bash
/usr/local/bin/python3 -m pip install -r requirements.txt
```

### 2. Configure Environment

Make sure your `.env` file in the parent directory has:

```bash
ANTHROPIC_API_KEY=your-api-key-here
CLAUDE_SKILL_ID=your-skill-id-here
```

Optional web app settings:

```bash
WEB_APP_HOST=127.0.0.1
WEB_APP_PORT=8000
```

### 3. Run the Application

```bash
python app.py
```

Or:

```bash
uvicorn app:app --reload
```

### 4. Open in Browser

Navigate to: `http://localhost:8000`

## Usage

### Sending Messages

1. Select a skill from the sidebar (or leave as "No Skill" for standard Claude)
2. Type your message in the input box
3. Press Enter or click "Send"

### Attaching Files

1. Click the 📎 button
2. Select one or more files
3. Files will appear in the preview area
4. Send your message with the attachments

### Adjusting Parameters

- **Temperature**: Use the slider (0.0 = focused, 2.0 = creative)
- **Max Tokens**: Set the maximum response length

### Exporting Chat

1. Click the "📥 Export Chat" button
2. Your chat will download as a markdown file with timestamp

### Clearing Chat

1. Click the "🗑️ Clear" button
2. Confirm to start a new session

## File Structure

```
web_app/
├── app.py                 # FastAPI backend
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── static/
│   ├── index.html        # Main HTML
│   ├── style.css         # Styling
│   └── app.js            # Frontend logic
└── uploads/              # Temporary file storage
```

## API Endpoints

- `GET /` - Serve main HTML page
- `GET /api/skills` - List available skills
- `POST /api/chat` - Send message to Claude
- `POST /api/upload` - Upload file
- `GET /api/export/{session_id}` - Export chat as markdown

## Troubleshooting

### Port Already in Use

Change the port in `.env`:

```bash
WEB_APP_PORT=8001
```

### API Key Error

Make sure your `.env` file has a valid `ANTHROPIC_API_KEY`.

### Skills Not Loading

Check that your API key has access to the Skills API beta.

## Development

To run in development mode with auto-reload:

```bash
uvicorn app:app --reload --host 127.0.0.1 --port 8000
```

## Security Note

⚠️ This is designed for **local/personal use**. Do not expose this to the public internet without:
- Proper authentication
- Rate limiting
- Input validation
- Secure API key management

## License

MIT
