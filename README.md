# Claude Skills API Starter Kit

A complete starter kit for working with the Anthropic Claude Skills API, including Python scripts, comprehensive documentation, and a modern web interface.

## 🚀 Quick Start

### 1. Clone or Download This Repository

```bash
git clone <your-repo-url>
cd claude-skills-experiment-02.06.26
```

### 2. Set Up Environment

Copy the example environment file:

```bash
cp .env.example .env
```

**Note:** For the web interface, you don't need to configure `.env` - users will enter their API keys directly in the browser.

### 3. Install Python Dependencies

```bash
pip install -r web_app/requirements.txt
```

### 4. Run the Web Interface

```bash
cd web_app
python app.py
```

Open your browser to `http://localhost:8000` and enter your Anthropic API key in the settings modal.

## 📁 What's Included

### 📚 Documentation

- **[API_CLAUDE_SKILLS_STARTER.md](API_CLAUDE_SKILLS_STARTER.md)** - Complete guide to the Claude Skills API
- **[ANTHROPIC_API_HYPERPARAMETERS.md](ANTHROPIC_API_HYPERPARAMETERS.md)** - Comprehensive hyperparameter reference
- **[USE_CASES.md](USE_CASES.md)** - Why and when to use the API vs web interface

### 🐍 Python Scripts

Located in `scripts/`:

- **`list_skills.py`** - Lists all available Claude Skills (custom + pre-built)
- **`test_skill.py`** - Tests a specific skill with a query

Both scripts save output to timestamped markdown files (`response_YY.MM.DD.HH.MM.SS.md`).

### 🌐 Web Interface

Located in `web_app/`:

A modern, full-featured web application for interacting with Claude Skills:

- 💬 **Chat Interface** - Beautiful dark mode UI with message bubbles
- 📎 **File Attachments** - Upload and attach files to messages
- 🎯 **Skill Selection** - Choose from your custom and pre-built skills
- ⚙️ **Hyperparameter Controls** - Adjust temperature (0.0-2.0) and max tokens
- 📥 **Export to Markdown** - Download entire chat history
- 📊 **Session Stats** - Track message count and token usage
- 🔒 **Secure** - API keys stored only in browser localStorage

See [web_app/README.md](web_app/README.md) for detailed documentation.

## 🎯 Usage Examples

### Using Python Scripts

**List your skills:**
```bash
python scripts/list_skills.py
```

**Test a skill:**
```bash
python scripts/test_skill.py
```

### Using the Web Interface

1. Start the server: `cd web_app && python app.py`
2. Open browser to `http://localhost:8000`
3. Click "⚙️ Settings" and enter your Anthropic API key
4. Select a skill from the sidebar
5. Start chatting!

## 🔑 Getting Your API Key

1. Go to [console.anthropic.com](https://console.anthropic.com/)
2. Sign in or create an account
3. Navigate to API Keys
4. Create a new API key
5. Copy the key (starts with `sk-ant-`)

## 📝 Important Notes

### OpenRouter Compatibility

❌ **Claude Skills are NOT accessible via OpenRouter** - you must use the direct Anthropic API.

### Skill Privacy

🔒 Skills are **workspace-scoped** - they're private to your Anthropic account. To share a skill:
- Share the actual skill files (SKILL.md, scripts/, etc.)
- Add collaborators to your workspace
- Use Team/Enterprise plans for organization-wide provisioning

### TypingMind Support

⚠️ TypingMind does not currently support the Skills API (feature requested but not implemented).

## 🛠️ Technical Details

### API Requirements

- Direct Anthropic API access
- Beta headers: `code-execution-2025-08-25`, `skills-2025-10-02`
- Code execution tool must be enabled
- Up to 8 skills per request
- Claude 4 supports up to 64,000 output tokens

### Web Interface Architecture

- **Backend:** FastAPI (Python)
- **Frontend:** Vanilla HTML/CSS/JavaScript
- **Styling:** Dark mode with glassmorphism effects
- **Security:** API keys stored in browser localStorage, never on server

## 📊 File Structure

```
claude-skills-experiment-02.06.26/
├── README.md                          # This file
├── API_CLAUDE_SKILLS_STARTER.md       # API guide
├── ANTHROPIC_API_HYPERPARAMETERS.md   # Hyperparameter reference
├── USE_CASES.md                       # Use case documentation
├── .env.example                       # Environment template
├── .gitignore                         # Git ignore rules
├── scripts/
│   ├── list_skills.py                 # List skills script
│   └── test_skill.py                  # Test skill script
├── web_app/
│   ├── app.py                         # FastAPI backend
│   ├── requirements.txt               # Python dependencies
│   ├── README.md                      # Web app docs
│   ├── static/
│   │   ├── index.html                 # Main HTML
│   │   ├── style.css                  # Styling
│   │   └── app.js                     # Frontend logic
│   └── uploads/                       # Temporary file storage
└── output/                            # Script output files
```

## 🔧 Configuration

### Environment Variables (Optional for Python Scripts)

```bash
# Only needed if using Python scripts with .env
ANTHROPIC_API_KEY=sk-ant-...
CLAUDE_SKILL_ID=skill_01...

# Web app configuration (optional)
WEB_APP_HOST=127.0.0.1
WEB_APP_PORT=8000
```

### Web Interface Settings

The web interface uses browser localStorage for configuration:
- **API Key:** Stored securely in browser, sent directly to Anthropic
- **Default Skill ID:** Optional, auto-selected on startup

## 🚨 Troubleshooting

### Port Already in Use

Change the port:
```bash
WEB_APP_PORT=8001 python app.py
```

### API Key Error

- Verify your key starts with `sk-ant-`
- Check that your key has Skills API access
- Ensure you're using the direct Anthropic API (not OpenRouter)

### Skills Not Loading

- Confirm your API key has beta access to Skills API
- Check browser console for errors
- Verify network connectivity

## 🎓 Learning Resources

- [Anthropic Skills Documentation](https://docs.anthropic.com/en/docs/build-with-claude/agent-skills)
- [Claude API Reference](https://docs.anthropic.com/en/api)
- [Skills GitHub Repository](https://github.com/anthropics/skills)

## 📄 License

MIT License - feel free to use this starter kit for your own projects!

## 🤝 Contributing

This is a starter kit template. Feel free to fork and customize for your needs!

## ⚠️ Security Notice

**For Local/Personal Use Only**

This starter kit is designed for local development and personal use. Before deploying to production:

- Implement proper authentication
- Add rate limiting
- Validate all inputs
- Use secure API key management
- Add HTTPS/TLS encryption
- Implement proper error handling
- Add logging and monitoring

## 🎉 Getting Started

Ready to build with Claude Skills? 

1. **Start with the web interface** - easiest way to experiment
2. **Read the documentation** - understand the API capabilities
3. **Explore use cases** - see what's possible
4. **Build something amazing!** 🚀

---

**Questions or Issues?** Check the documentation files or refer to the [Anthropic documentation](https://docs.anthropic.com/).
