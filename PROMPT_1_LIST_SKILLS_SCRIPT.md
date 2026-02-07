# Prompt 1: Claude Skills List Script

I need you to create a Python script that lists all available Claude Skills from the Anthropic API.

## Requirements

### 1. Environment Setup

Create a `.env` file with:
```
ANTHROPIC_API_KEY=sk-ant-your-key-here
```

Create a `.env.example` template with:
```
# Anthropic API Configuration
ANTHROPIC_API_KEY=sk-ant-...

# Optional: Default skill ID for testing
CLAUDE_SKILL_ID=skill_01...
```

### 2. Python Script: `list_skills.py`

**Functionality:**
- Connect to Anthropic API using the `anthropic` Python library
- List all available Claude Skills (both custom and pre-built)
- Display skills in a formatted, readable way
- Save output to a timestamped markdown file with format: `response_YY.MM.DD.HH.MM.SS.md`
- Display the output to console AND save to file

**API Details:**
- Use the Skills API beta: `betas=["skills-2025-10-02"]`
- Endpoint: `client.beta.skills.list()`
- Each skill has: `id`, `display_title`, `source` (type), and optional `description`

**Output Format:**

The script should display:
```
# Claude Skills List

🔍 Fetching your Claude Skills...

================================================================================
📦 CUSTOM SKILLS
================================================================================

✓ skill-name
  ID: skill_01...
  Description: [description or "N/A"]
  Version: latest

================================================================================
🏢 ANTHROPIC PRE-BUILT SKILLS
================================================================================

✓ xlsx
  ID: xlsx
  Description: N/A

[etc...]

================================================================================
📊 SUMMARY: X custom, Y pre-built
================================================================================

✅ Output saved to: response_26.02.06.16.43.50.md
```

**File Naming:**
- Use `datetime.now().strftime("%y.%m.%d.%H.%M.%S")` for timestamp
- Format: `response_YY.MM.DD.HH.MM.SS.md`

### 3. Dependencies

Install via pip:
```bash
pip install anthropic python-dotenv
```

Or create `requirements.txt`:
```
anthropic==0.78.0
python-dotenv==1.0.1
```

### 4. Error Handling

- Check if `.env` file exists
- Validate API key is present
- Handle API errors gracefully
- Display helpful error messages

### 5. Code Structure

```python
import os
from datetime import datetime
from dotenv import load_dotenv
import anthropic

# Load environment
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

# Validate API key
if not api_key:
    print("❌ Error: ANTHROPIC_API_KEY not found in .env file")
    exit(1)

# Create client
client = anthropic.Anthropic(api_key=api_key)

# Fetch skills
skills_response = client.beta.skills.list(betas=["skills-2025-10-02"])

# Format output
# ... (separate custom vs pre-built)

# Save to file
timestamp = datetime.now().strftime("%y.%m.%d.%H.%M.%S")
filename = f"response_{timestamp}.md"

# Write to file and display
```

## Expected Behavior

When run:
1. Loads API key from `.env`
2. Connects to Anthropic API
3. Fetches all skills
4. Displays formatted output to console
5. Saves same output to timestamped markdown file
6. Reports the filename

## Testing

After creating the script:
1. Run: `python list_skills.py`
2. Verify console output is formatted correctly
3. Verify markdown file is created with timestamp
4. Verify file contains the same content as console

## Notes

- Skills with `source="custom"` are user-created
- Skills with `source="anthropic"` are pre-built
- The API requires direct Anthropic access (NOT OpenRouter)
- Beta headers are required for Skills API access
