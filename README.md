# Claude LangGraph Headless

A robust, reusable LangGraph node for calling Claude Code in headless mode. Available in both **TypeScript** and **Python**.

## Features

- 🚀 **Robust Process Management** - Uses `spawn()`/`Popen()` for better control
- 📝 **Large Prompt Support** - Uses stdin for prompts of any size (no command-line limits)
- 🔄 **Automatic Retries** - Configurable retry logic with exponential backoff
- 🔐 **Auth Management** - Automatically uses subscription instead of API billing
- ⚙️ **Configurable** - Timeout, buffer size, output format, retries
- 🧪 **Well Tested** - Comprehensive test suites for both languages
- 📦 **LangGraph Ready** - Drop-in node for your workflows

## Installation

### TypeScript
```bash
npm install @biosphere-labs/claude-langgraph-headless
```

### Python
```bash
pip install claude-langgraph-headless
```

## Quick Start

### TypeScript

```typescript
import { ClaudeHeadlessNode } from '@biosphere-labs/claude-langgraph-headless';

// Create a LangGraph node
const claudeNode = new ClaudeHeadlessNode({
  outputFormat: 'json',
  timeout: 180000,
  useSubscription: true
});

// Use in your LangGraph workflow
const result = await claudeNode.invoke({
  systemPrompt: "You are a helpful assistant.",
  userPrompt: "Analyze this data..."
});
```

### Python

```python
from claude_langgraph_headless import ClaudeHeadlessNode, ClaudeHeadlessOptions, ClaudeHeadlessInput

# Create a LangGraph node
claude_node = ClaudeHeadlessNode(
    ClaudeHeadlessOptions(
        output_format="json",
        timeout=180,
        use_subscription=True
    )
)

# Use in your LangGraph workflow
result = await claude_node.ainvoke(
    ClaudeHeadlessInput(
        system_prompt="You are a helpful assistant.",
        user_prompt="Analyze this data..."
    )
)
```

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `outputFormat` | `'text' \| 'json' \| 'stream-json'` | `'json'` | Claude output format |
| `timeout` | `number` | `180000`ms (TS)<br>`180`s (Python) | Max execution time |
| `maxBuffer` | `number` | `10MB` | Max stdout buffer size |
| `useSubscription` | `boolean` | `true` | Use subscription vs API billing |
| `retries` | `number` | `0` | Number of retry attempts |

## LangGraph Integration Example

### TypeScript with LangGraph

```typescript
import { StateGraph } from "@langchain/langgraph";
import { ClaudeHeadlessNode } from '@biosphere-labs/claude-langgraph-headless';

// Define your state
interface WorkflowState {
  input: string;
  result?: string;
}

// Create the Claude node
const claudeNode = new ClaudeHeadlessNode({
  outputFormat: 'json',
  timeout: 180000,
  useSubscription: true
});

// Build your workflow
const workflow = new StateGraph<WorkflowState>({
  channels: {
    input: null,
    result: null
  }
});

workflow.addNode("analyze", async (state: WorkflowState) => {
  const response = await claudeNode.invoke({
    systemPrompt: "You are a data analyst.",
    userPrompt: state.input
  });
  return { ...state, result: response.result };
});

workflow.setEntryPoint("analyze");
workflow.setFinishPoint("analyze");

const app = workflow.compile();
```

### Python with LangGraph

```python
from langgraph.graph import StateGraph
from typing import TypedDict
from claude_langgraph_headless import ClaudeHeadlessNode, ClaudeHeadlessOptions, ClaudeHeadlessInput

# Define your state
class WorkflowState(TypedDict):
    input: str
    result: str

# Create the Claude node
claude_node = ClaudeHeadlessNode(
    ClaudeHeadlessOptions(
        output_format="json",
        timeout=180,
        use_subscription=True
    )
)

# Define node function
async def analyze(state: WorkflowState) -> WorkflowState:
    response = await claude_node.ainvoke(
        ClaudeHeadlessInput(
            system_prompt="You are a data analyst.",
            user_prompt=state["input"]
        )
    )
    return {"result": response["result"]}

# Build workflow
workflow = StateGraph(WorkflowState)
workflow.add_node("analyze", analyze)
workflow.set_entry_point("analyze")
workflow.set_finish_point("analyze")

app = workflow.compile()
```

## Architecture

### Why `spawn()`/`Popen()` instead of `exec()`?

- ✅ **No command-line length limits** - Prompts sent via stdin using temp files
- ✅ **Better stream control** - Separate handling of stdin/stdout/stderr
- ✅ **Proper timeout handling** - Graceful termination with forced kill fallback
- ✅ **Buffer overflow protection** - Configurable max buffer size
- ✅ **Better error reporting** - Captures stderr separately

### Authentication Strategy

The package automatically uses your Claude subscription instead of API billing by unsetting `ANTHROPIC_API_KEY` in the child process environment when `useSubscription: true`.

## Error Handling

The package handles:
- **Timeouts** - Graceful termination with configurable timeout
- **Credit balance errors** - Detects low credit balance from Claude output
- **Buffer overflows** - Prevents memory issues with large outputs
- **Process failures** - Captures exit codes and stderr
- **Retry logic** - Optional exponential backoff retries

## Testing

### TypeScript
```bash
npm test
```

### Python
```bash
cd python
pytest
```

## Examples

See `/examples` directory for:
- Basic usage patterns
- LangGraph integration examples
- Error handling strategies
- Custom configuration options

## Requirements

- Claude Code CLI must be installed and available in PATH
- Node.js 20+ (for TypeScript version)
- Python 3.8+ (for Python version)

## License

MIT

## Contributing

Contributions welcome! Please open an issue or PR.
