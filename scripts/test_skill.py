#!/usr/bin/env python3
"""
Test the automatic-book-machine-v2 skill by asking what it can do.
"""

import os
from datetime import datetime
from dotenv import load_dotenv
import anthropic

# Load environment variables
load_dotenv()

def main():
    # Generate timestamp for output file
    timestamp = datetime.now().strftime("%y.%m.%d.%H.%M.%S")
    
    # Ensure output directory exists
    output_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, f"response_{timestamp}.md")
    
    # Collect output lines
    output_lines = []
    
    api_key = os.getenv("ANTHROPIC_API_KEY")
    skill_id = os.getenv("CLAUDE_SKILL_ID")
    
    if not api_key or api_key == "your-api-key-here":
        msg = "❌ Error: Please set ANTHROPIC_API_KEY in .env"
        print(msg)
        output_lines.append(msg)
        with open(output_file, 'w') as f:
            f.write(msg)
        return
    
    if not skill_id or skill_id.startswith("skill_01AbCdEfGhIjKlMnOpQrStUv"):
        msg = "❌ Error: Please set CLAUDE_SKILL_ID in .env"
        print(msg)
        output_lines.append(msg)
        with open(output_file, 'w') as f:
            f.write(msg)
        return
    
    # Initialize client
    client = anthropic.Anthropic(api_key=api_key)
    
    header = f"# Testing automatic-book-machine-v2 Skill\n\n🤖 Testing automatic-book-machine-v2 skill...\n📋 Skill ID: {skill_id}\n\n" + "=" * 80 + "\nQUESTION: What can you do with the automatic-book-machine-v2 skill?\n" + "=" * 80 + "\n"
    print(header)
    output_lines.append(header)
    
    try:
        # Create a message with the skill enabled
        response = client.beta.messages.create(
            model="claude-opus-4-6",
            max_tokens=4096,
            betas=["code-execution-2025-08-25", "skills-2025-10-02"],
            container={
                "skills": [
                    {
                        "type": "custom",
                        "skill_id": skill_id,
                        "version": "latest"
                    }
                ]
            },
            messages=[{
                "role": "user", 
                "content": "What can you do with the automatic-book-machine-v2 skill? Please describe its capabilities and what tasks it can help with."
            }],
            tools=[{"type": "code_execution_20250825", "name": "code_execution"}]
        )
        
        # Print the response
        response_header = "\n🎯 RESPONSE:\n"
        print(response_header)
        output_lines.append(response_header)
        
        for block in response.content:
            if hasattr(block, 'text'):
                print(block.text)
                output_lines.append(block.text)
            elif block.type == 'tool_use':
                tool_info = f"\n[Tool Used: {block.name}]"
                print(tool_info)
                output_lines.append(tool_info)
                if hasattr(block, 'input'):
                    input_info = f"Input: {block.input}"
                    print(input_info)
                    output_lines.append(input_info)
        
        footer = "\n" + "=" * 80 + f"\n📊 Usage: {response.usage.input_tokens} input tokens, {response.usage.output_tokens} output tokens\n" + "=" * 80
        print(footer)
        output_lines.append(footer)
        
        # Write to file
        with open(output_file, 'w') as f:
            f.write('\n'.join(output_lines))
        print(f"\n💾 Output saved to: {output_file}")
        
    except anthropic.BadRequestError as e:
        error = f"❌ API Error: {e}\n\nPossible issues:\n  - Skill ID might be invalid\n  - Beta features might not be enabled"
        print(error)
        output_lines.append(error)
        with open(output_file, 'w') as f:
            f.write('\n'.join(output_lines))
    except Exception as e:
        error = f"❌ Unexpected error: {e}"
        print(error)
        output_lines.append(error)
        with open(output_file, 'w') as f:
            f.write('\n'.join(output_lines))

if __name__ == "__main__":
    main()
