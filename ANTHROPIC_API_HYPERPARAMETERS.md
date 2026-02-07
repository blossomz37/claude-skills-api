# Anthropic Claude API Hyperparameters Reference

## 🎛️ Core Inference Parameters

### `temperature`
- **Range**: `0.0` to `2.0` (some sources say `1.0` max, but newer models support up to `2.0`)
- **Default**: `1.0`
- **Purpose**: Controls randomness in responses
  - **Lower values** (0.0–0.3): More deterministic, analytical, focused outputs
  - **Higher values** (0.7–2.0): More creative, varied, exploratory outputs
- **Note**: Even at `0.0`, results may not be fully deterministic
- **Recommendation**: Adjust either `temperature` OR `top_p`, not both

### `top_p` (Nucleus Sampling)
- **Range**: `0.1` to `1.0`
- **Default**: Not specified (typically `1.0`)
- **Purpose**: Cumulative probability cutoff for token selection
  - `0.1` = Only consider top 10% most probable tokens
  - `1.0` = Consider all tokens
- **Lower values**: Less diversity, more focused
- **Higher values**: More diversity, more varied
- **Recommendation**: Adjust either `temperature` OR `top_p`, not both

### `top_k`
- **Range**: Integer values
- **Default**: Not specified
- **Purpose**: Sample from the `k` most likely next tokens
- **Lower values**: More focused, less varied
- **Higher values**: More diverse
- **Note**: ⚠️ **NOT supported in standard Claude API** (only available in some third-party implementations)
- **Recommendation**: Use `temperature` instead for most use cases

### `max_tokens`
- **Range**: `1` to model-specific maximum
  - Claude 3.7 and 4: Up to **64,000 tokens** for output
- **Purpose**: Absolute upper limit on response length
- **Behavior**: Model may stop before reaching this limit if:
  - Response is naturally complete
  - Stop sequence is encountered
- **Note**: For extended thinking models, includes "thinking budget tokens"

## 🔧 Request Configuration Parameters

### `model`
- **Required**: Yes
- **Purpose**: Specifies which Claude model to use
- **Examples**: `"claude-opus-4-6"`, `"claude-sonnet-4-20250514"`, `"claude-haiku-4-20250611"`

### `system`
- **Type**: String
- **Purpose**: Sets the system prompt for the conversation
- **Use case**: Define assistant behavior, role, constraints

### `stop_sequences`
- **Type**: Array of strings
- **Purpose**: Custom stopping points for generation
- **Example**: `["END", "STOP", "\n\n---"]`

### `stream`
- **Type**: Boolean
- **Default**: `false`
- **Purpose**: Enable server-sent events (SSE) for streaming responses

### `inference_geo`
- **Type**: String (optional)
- **Purpose**: Data residency controls - specify where model inference runs
- **Use case**: Compliance with regional data requirements

## 🛠️ Tool Use Parameters

### `tools`
- **Type**: Array of tool definitions
- **Purpose**: Define available functions with name, description, and input_schema
- **Example**:
  ```json
  {
    "name": "get_weather",
    "description": "Get current weather for a location",
    "input_schema": {
      "type": "object",
      "properties": {
        "location": {"type": "string"}
      }
    }
  }
  ```

### `tool_choice`
- **Options**:
  - `"none"`: No tool use
  - `"auto"`: Model decides when to use tools
  - `"required"`: Must call at least one tool
  - `{"type": "tool", "name": "tool_name"}`: Force specific tool
- **Default**: `"auto"`

### `parallel_tool_calls`
- **Type**: Boolean
- **Purpose**: Enable or disable parallel function calling during tool use

## 🎓 Skills API Parameters

### `container.skills`
- **Type**: Array of skill objects (max 8)
- **Purpose**: Reference Claude Skills to use in the request
- **Required fields per skill**:
  - `type`: `"custom"` or `"anthropic"`
  - `skill_id`: Skill identifier
  - `version`: Version number or `"latest"`
- **Example**:
  ```json
  {
    "skills": [
      {
        "type": "custom",
        "skill_id": "skill_THISxISxNOTxREALxIS24xCH",
        "version": "latest"
      }
    ]
  }
  ```

## 📊 Best Practices

### Temperature Guidelines
| Use Case                  | Recommended Temperature |
| ------------------------- | ----------------------- |
| Code generation           | 0.0 - 0.3               |
| Data analysis             | 0.0 - 0.3               |
| Multiple choice questions | 0.0 - 0.2               |
| Technical documentation   | 0.3 - 0.5               |
| General conversation      | 0.7 - 1.0               |
| Creative writing          | 0.8 - 1.5               |
| Brainstorming             | 1.0 - 2.0               |

### Parameter Combinations
- ✅ **Good**: Adjust `temperature` alone
- ✅ **Good**: Adjust `top_p` alone
- ⚠️ **Caution**: Adjusting both `temperature` and `top_p` simultaneously
- ❌ **Not Supported**: Using `top_k` with standard Anthropic API

### Token Budget
- Always set `max_tokens` to a reasonable value
- Consider cost implications (output tokens are billed)
- For extended thinking: "thinking budget tokens" are subset of `max_tokens`

## 🔗 Additional Resources

- [Anthropic API Documentation](https://platform.claude.com/docs/en/api/overview)
- [Model Parameters Guide](https://docs.aws.amazon.com/bedrock/latest/userguide/model-parameters-claude.html)
- [Skills API Guide](https://platform.claude.com/docs/en/build-with-claude/skills-guide)
