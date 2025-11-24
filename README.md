# Claude LangGraph Headless

A robust, reusable LangGraph node for calling Claude Code in headless mode. Available in both **TypeScript** and **Python**.

## Features

- 🚀 **Robust Process Management** - Uses `spawn` instead of `exec` for better control
- 📝 **Streaming Support** - Optional streaming of responses
- 🔄 **Automatic Retries** - Configurable retry logic
- 💾 **Large Prompt Handling** - Uses stdin for prompts of any size
- 🔐 **Auth Management** - Automatically uses subscription instead of API billing
- ⚙️ **Configurable** - Timeout, buffer size, output format
- 🧪 **Well Tested** - Comprehensive test suites
- 📦 **LangGraph Ready** - Drop-in node for your workflows

## Installation

### TypeScript
```bash
npm install @anthropic/claude-langgraph-headless
```

### Python
```bash
pip install claude-langgraph-headless
```

## Quick Start

### TypeScript

```typescript
import { ClaudeHeadlessNode } from '@anthropic/claude-langgraph-headless';

// Create a LangGraph node
const claudeNode = new ClaudeHeadlessNode({
  outputFormat: 'json',
  timeout: 180000,
  useSubscription: true
});

// Use in your LangGraph workflow
const result = await claudeNode.invoke({
  systemPrompt: "You are a helpful assistant.",
  userPrompt: "Analyze this conversation..."
});
```

### Python

```python
from claude_langgraph_headless import ClaudeHeadlessNode

# Create a LangGraph node
claude_node = ClaudeHeadlessNode(
    output_format="json",
    timeout=180,
    use_subscription=True
)

# Use in your LangGraph workflow
result = await claude_node.ainvoke({
    "system_prompt": "You are a helpful assistant.",
    "user_prompt": "Analyze this conversation..."
})
```

## Architecture

Uses `child_process.spawn` (TypeScript) / `subprocess.Popen` (Python) instead of `exec` for:
- Better control over stdin/stdout/stderr
- No command-line length limits
- Proper stream handling
- Better error reporting
- Process lifecycle management

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `outputFormat` | `'text' \| 'json' \| 'stream-json'` | `'json'` | Claude output format |
| `timeout` | `number` | `180000` (3min) | Max execution time (ms) |
| `maxBuffer` | `number` | `10MB` | Max stdout buffer size |
| `useSubscription` | `boolean` | `true` | Use subscription vs API billing |
| `retries` | `number` | `0` | Number of retry attempts |

## Examples

See `/examples` directory for:
- Basic usage
- LangGraph integration
- Streaming responses
- Error handling
- Custom configurations

## Testing

### TypeScript
```bash
npm test
```

### Python
```bash
pytest
```

## License

MIT
