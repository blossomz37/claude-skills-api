# How to Access Claude Skills with Your Anthropic API Key

## Key Requirements

1. **API Key** - Your Anthropic API key from the console
2. **Beta Headers** - You must enable these specific betas in your API requests:
   - `code-execution-2025-08-25`
   - `skills-2025-10-02`
   - `files-api-2025-04-14` (optional, for file handling)
3. **Code Execution Tool** - Skills require the code execution tool to be enabled

## Skill ID Format

- **Anthropic Pre-built Skills**: Short names like `"xlsx"`, `"pptx"`, `"docx"`, `"pdf"`
- **Custom Skills**: Generated IDs like `"skill_01AbCdEfGhIjKlMnOpQrStUv"`

## Python Example - Using Skills

```python
import anthropic

client = anthropic.Anthropic(api_key="your-api-key-here")

response = client.beta.messages.create(
    model="claude-opus-4-6",
    max_tokens=4096,
    betas=["code-execution-2025-08-25", "skills-2025-10-02"],
    container={
        "skills": [
            {
                "type": "custom",  # or "anthropic" for pre-built
                "skill_id": "skill_01AbCdEfGhIjKlMnOpQrStUv",  # Your skill ID
                "version": "latest"  # or specific version timestamp
            }
        ]
    },
    messages=[{"role": "user", "content": "Use the skill to analyze this data."}],
    tools=[{"type": "code_execution_20250825", "name": "code_execution"}]
)
```

## Finding Your Skill IDs

```python
# List all skills (custom + pre-built)
skills = client.beta.skills.list(betas=["skills-2025-10-02"])
for skill in skills.data:
    print(f"{skill.id}: {skill.display_title} (source: {skill.source})")

# List only your custom skills
custom_skills = client.beta.skills.list(source="custom", betas=["skills-2025-10-02"])
```

## Creating Custom Skills

```python
from anthropic.lib import files_from_dir

skill = client.beta.skills.create(
    display_title="Your Skill Name",
    files=files_from_dir("/path/to/skill/folder"),
    betas=["skills-2025-10-02"]
)
print(skill.id)  # This is your skill_id to use in API calls
```

## Custom Skill Structure

Your skill folder must contain:

- **`SKILL.md`** (required) - Instructions with YAML frontmatter:
  ```yaml
  ---
  name: your-skill-name  # lowercase, hyphens only, max 64 chars
  description: What this skill does  # max 1024 chars, used by Claude to decide when to activate
  ---
  # Your skill instructions here
  ```
- **`scripts/`** (optional) - Python/Bash executables
- **`references/`** (optional) - Documentation
- **`assets/`** (optional) - Templates, fonts, etc.

## Important Notes

- You can use up to **8 skills per request**
- Skills are **private to your workspace** when created via API
- The `description` field is crucial - Claude uses it to determine skill relevance
- Skills execute in a sandboxed environment via code execution
