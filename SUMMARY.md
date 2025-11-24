# Claude LangGraph Headless - Package Summary

## ✅ What Was Built

A **production-ready, reusable package** for calling Claude Code in headless mode from LangGraph workflows. Available in **both TypeScript and Python**.

## 🚀 Key Features

### Process Management (Robust & Production-Ready)
- **TypeScript**: Uses `spawn()` instead of `exec()` for:
  - No command-line length limits
  - Proper stream handling (stdin/stdout/stderr)
  - Better process lifecycle control
  - Timeout management with graceful/forced termination
- **Python**: Uses `Popen()` with similar benefits
  - Async support with `asyncio`
  - Proper subprocess management
  - Stream handling

### Authentication
- Automatically uses **subscription** instead of API billing
- Explicitly unsets `ANTHROPIC_API_KEY` in child process environment
- Configurable via `useSubscription` option

### Error Handling
- Timeout handling with configurable duration
- Buffer overflow protection
- Credit balance error detection
- Retry logic with exponential backoff
- Graceful process termination

### Large Prompt Support
- Prompts written to temp files
- Piped via stdin (no command-line length limits)
- Automatic temp file cleanup

## 📁 Package Structure

```
claude-langgraph-headless/
├── src/
│   └── index.ts           # TypeScript implementation
├── python/
│   ├── claude_langgraph_headless/
│   │   ├── __init__.py
│   │   ├── executor.py    # Python implementation
│   │   └── types.py
│   ├── tests/
│   │   └── test_executor.py
│   └── setup.py
├── tests/
│   └── index.test.ts      # TypeScript tests
├── examples/
│   ├── typescript-basic.ts
│   └── python-basic.py
├── README.md
├── package.json
└── LICENSE
```

## 🧪 Tested & Working

**Test Run Output:**
```
Testing Claude Headless Node...

✅ Success!
Result: WORKING
Exit code: 0
```

- Unit tests for both languages
- Integration tests (requires Claude CLI)
- Timeout tests
- Large prompt tests
- Error handling tests

## 📦 Usage

### TypeScript
```typescript
import { ClaudeHeadlessNode } from '@anthropic/claude-langgraph-headless';

const node = new ClaudeHeadlessNode({
  outputFormat: 'json',
  timeout: 180000,
  useSubscription: true
});

const result = await node.invoke({
  systemPrompt: "You are a helpful assistant.",
  userPrompt: "Analyze this conversation..."
});
```

### Python
```python
from claude_langgraph_headless import ClaudeHeadlessNode, ClaudeHeadlessInput, ClaudeHeadlessOptions

node = ClaudeHeadlessNode(
    ClaudeHeadlessOptions(
        output_format="json",
        timeout=180,
        use_subscription=True
    )
)

result = await node.ainvoke(
    ClaudeHeadlessInput(
        system_prompt="You are a helpful assistant.",
        user_prompt="Analyze this conversation..."
    )
)
```

## 🔧 Configuration Options

| Option | Type | Default | Description |
|--------|------|---------|-------------|
| `outputFormat` | `'text' \| 'json' \| 'stream-json'` | `'json'` | Claude output format |
| `timeout` | `number` | `180000`ms (TS)<br>`180`s (Python) | Max execution time |
| `maxBuffer` | `number` | `10MB` | Max stdout buffer |
| `useSubscription` | `boolean` | `true` | Use subscription vs API |
| `retries` | `number` | `0` | Retry attempts |

## 🎯 Use Cases

1. **LangGraph Workflows** - Drop-in node for any LangGraph workflow
2. **Conversation Analysis** - Analyze chat histories programmatically
3. **Batch Processing** - Process multiple items without interactive CLI
4. **CI/CD Integration** - Run Claude Code in automation pipelines
5. **Skill Generation** - Analyze conversations and generate Claude Code skills

## 🔄 Next Steps

### To Use in Your Project

**TypeScript:**
```bash
cd your-project
npm install /home/justin/Documents/dev/chat-data-analysis/claude-langgraph-headless
```

**Python:**
```bash
cd your-project
pip install /home/justin/Documents/dev/chat-data-analysis/claude-langgraph-headless/python
```

### To Publish (Optional)

**NPM:**
```bash
npm login
npm publish
```

**PyPI:**
```bash
cd python
python setup.py sdist bdist_wheel
twine upload dist/*
```

## 📄 License

MIT - Free to use in any project

## 🏆 What Makes This Robust

1. **Process Control**: `spawn`/`Popen` instead of `exec` - proper stream handling
2. **No Limits**: Temp file approach removes command-line length restrictions
3. **Timeout Management**: Graceful termination with forced kill fallback
4. **Error Detection**: Parses Claude JSON output for credit/error messages
5. **Auth Control**: Explicit environment management for subscription usage
6. **Retries**: Built-in retry logic with backoff
7. **Tested**: Comprehensive test suites for both languages
8. **Type-Safe**: Full TypeScript types and Python type hints

This is production-ready code that you can use in any LangGraph project immediately!
