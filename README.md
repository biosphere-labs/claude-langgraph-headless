# Claude Headless Subscription

**Use Claude Code programmatically via your subscription instead of expensive API credits.** Available in TypeScript and Python.

## Why This Exists

Claude API credits are expensive. This package lets you make **headless/programmatic calls to Claude using your Claude subscription** instead of API keys - potentially saving hundreds of dollars.

**Key insight**: Claude Code can authenticate via OAuth (subscription) instead of API keys when using the `--settings` flag with an empty API key. This package automates that for you.

## Quick Start

### TypeScript
```bash
npm install @biosphere-labs/claude-headless-subscription
```

```typescript
import { ClaudeHeadlessNode } from '@biosphere-labs/claude-headless-subscription';

const claude = new ClaudeHeadlessNode({
  useSubscription: true,  // Uses subscription billing
  outputFormat: 'json'
});

const result = await claude.invoke({
  systemPrompt: "You are a helpful assistant.",
  userPrompt: "Analyze this data..."
});
```

### Python
```bash
pip install claude-headless-subscription
```

```python
from claude_headless_subscription import ClaudeHeadlessNode, ClaudeHeadlessOptions, ClaudeHeadlessInput

claude = ClaudeHeadlessNode(
    ClaudeHeadlessOptions(
        use_subscription=True,  # Uses subscription billing
        output_format="json"
    )
)

result = await claude.ainvoke(
    ClaudeHeadlessInput(
        system_prompt="You are a helpful assistant.",
        user_prompt="Analyze this data..."
    )
)
```

## How It Works

1. Uses `claude -p` (headless mode) with `--settings {"env": {"ANTHROPIC_API_KEY": ""}}`
2. Forces Claude Code to use OAuth credentials from `~/.claude/.credentials.json`
3. All costs billed to your Claude subscription, not API credits

## Use Cases

- **Automation workflows** - Build AI pipelines without API costs
- **Batch processing** - Process large datasets affordably
- **LangGraph integration** - Drop-in node for AI workflows
- **Development/testing** - Iterate without burning through credits
- **Personal projects** - Use your existing subscription

## Configuration

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `useSubscription` | boolean | `true` | Use subscription vs API billing |
| `outputFormat` | string | `'json'` | `'text'`, `'json'`, or `'stream-json'` |
| `timeout` | number | `180000`ms / `180`s | Max execution time |
| `retries` | number | `0` | Retry attempts on failure |

## LangGraph Integration

Works seamlessly as a LangGraph node:

```typescript
import { StateGraph } from "@langchain/langgraph";
import { ClaudeHeadlessNode } from '@biosphere-labs/claude-headless-subscription';

const claude = new ClaudeHeadlessNode({ useSubscription: true });

const workflow = new StateGraph({ /* ... */ });
workflow.addNode("analyze", async (state) => {
  return await claude.invoke({
    systemPrompt: "You are a data analyst.",
    userPrompt: state.input
  });
});
```

## Requirements

- Claude Code CLI installed and in PATH
- Authenticated Claude session (`~/.claude/.credentials.json`)
- Node.js 20+ (TypeScript) or Python 3.8+ (Python)

## Error Handling

Handles timeouts, buffer overflows, process failures, and low credit balance errors. Supports configurable retry logic with exponential backoff.

## SEO Keywords

Claude subscription, Claude headless mode, Claude programmatic access, Claude without API key, Claude automation, Claude batch processing, affordable Claude API alternative, Claude Code headless, Claude subscription billing

## License

MIT

## Contributing

Contributions welcome! Open an issue or PR at [github.com/biosphere-labs/claude-headless-subscription](https://github.com/biosphere-labs/claude-headless-subscription)
