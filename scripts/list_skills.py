#!/usr/bin/env python3
"""
List all Claude Skills available in your Anthropic account.
This script will show both custom and pre-built skills.
"""

import os
from datetime import datetime
from dotenv import load_dotenv
import anthropic

# Load environment variables from .env file
load_dotenv()

def main():
    # Generate timestamp for output file
    timestamp = datetime.now().strftime("%y.%m.%d.%H.%M.%S")
    output_file = f"response_{timestamp}.md"
    
    # Collect output lines
    output_lines = []
    
    # Get API key from environment
    api_key = os.getenv("ANTHROPIC_API_KEY")
    
    if not api_key:
        msg = "❌ Error: ANTHROPIC_API_KEY not found in .env file\nPlease copy .env.example to .env and add your API key"
        print(msg)
        output_lines.append(msg)
        with open(output_file, 'w') as f:
            f.write(msg)
        return
    
    if api_key == "your-api-key-here":
        msg = "❌ Error: Please replace 'your-api-key-here' with your actual Anthropic API key in .env"
        print(msg)
        output_lines.append(msg)
        with open(output_file, 'w') as f:
            f.write(msg)
        return
    
    # Initialize Anthropic client
    client = anthropic.Anthropic(api_key=api_key)
    
    header = "# Claude Skills List\n\n🔍 Fetching your Claude Skills...\n"
    print(header)
    output_lines.append(header)
    
    try:
        # List all skills (custom + pre-built)
        skills = client.beta.skills.list(betas=["skills-2025-10-02"])
        
        if not skills.data:
            msg = "No skills found in your account."
            print(msg)
            output_lines.append(msg)
            with open(output_file, 'w') as f:
                f.write('\n'.join(output_lines))
            return
        
        # Separate custom and pre-built skills
        custom_skills = [s for s in skills.data if s.source == "custom"]
        anthropic_skills = [s for s in skills.data if s.source == "anthropic"]
        
        # Display custom skills
        if custom_skills:
            section = "\n" + "=" * 80 + "\n📦 CUSTOM SKILLS\n" + "=" * 80
            print(section)
            output_lines.append(section)
            for skill in custom_skills:
                skill_info = f"\n✓ {skill.display_title}\n  ID: {skill.id}\n  Description: {getattr(skill, 'description', 'N/A')}\n  Version: {getattr(skill, 'version', 'latest')}"
                print(skill_info)
                output_lines.append(skill_info)
        
        # Display Anthropic pre-built skills
        if anthropic_skills:
            section = "\n" + "=" * 80 + "\n🏢 ANTHROPIC PRE-BUILT SKILLS\n" + "=" * 80
            print(section)
            output_lines.append(section)
            for skill in anthropic_skills:
                skill_info = f"\n✓ {skill.display_title}\n  ID: {skill.id}\n  Description: {getattr(skill, 'description', 'N/A')}"
                print(skill_info)
                output_lines.append(skill_info)
        
        # Summary
        summary = f"\n" + "=" * 80 + f"\n📊 SUMMARY: {len(custom_skills)} custom, {len(anthropic_skills)} pre-built\n" + "=" * 80
        print(summary)
        output_lines.append(summary)
        
        # Check if the skill ID in .env exists
        env_skill_id = os.getenv("CLAUDE_SKILL_ID")
        if env_skill_id and env_skill_id != "skill_01AbCdEfGhIjKlMnOpQrStUv":
            skill_ids = [s.id for s in skills.data]
            if env_skill_id in skill_ids:
                validation = f"\n✅ Your .env CLAUDE_SKILL_ID ({env_skill_id}) is valid!"
                print(validation)
                output_lines.append(validation)
            else:
                validation = f"\n⚠️  Warning: CLAUDE_SKILL_ID in .env ({env_skill_id}) not found in your account\n   Available skill IDs listed above."
                print(validation)
                output_lines.append(validation)
        
        # Write to file
        with open(output_file, 'w') as f:
            f.write('\n'.join(output_lines))
        print(f"\n💾 Output saved to: {output_file}")
        
    except anthropic.BadRequestError as e:
        error = f"❌ API Error: {e}\n\nThis might mean:\n  - Your API key is invalid\n  - Skills API access is not enabled for your account"
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
