# Integrating with analysis-workflow

## How to Use This Package in Your Analysis Workflow

### TypeScript Integration

Replace the old `claude-headless.ts` utility with this package:

**Before:**
```typescript
// src/utils/claude-headless.ts
import { exec } from "child_process";
// ... messy exec implementation
```

**After:**
```typescript
// Install the package
npm install /path/to/claude-langgraph-headless

// src/utils/claude-headless.ts
import { ClaudeHeadlessExecutor } from '@anthropic/claude-langgraph-headless';

const executor = new ClaudeHeadlessExecutor({
  outputFormat: 'json',
  timeout: 180000,
  useSubscription: true,
});

export async function callClaudeHeadless(
  systemPrompt: string,
  userPrompt: string
): Promise<string> {
  const result = await executor.execute({
    systemPrompt,
    userPrompt,
  });
  return result.result;
}
```

### Python LangGraph Integration

```python
from claude_langgraph_headless import ClaudeHeadlessNode, ClaudeHeadlessOptions

# Create node for your LangGraph
analyzer_node = ClaudeHeadlessNode(
    ClaudeHeadlessOptions(
        output_format="json",
        timeout=180,
        use_subscription=True
    )
)

# Use in your StateGraph
from langgraph.graph import StateGraph

workflow = StateGraph(YourState)
workflow.add_node("analyze", lambda state: analyzer_node.invoke({
    "system_prompt": get_analysis_prompt(),
    "user_prompt": state["conversation"]
}))
```

## Benefits Over Old Implementation

1. ✅ **No command-line length limits** - Uses stdin instead of arguments
2. ✅ **Better error handling** - Detects credit errors, timeouts, etc.
3. ✅ **Proper process control** - spawn/Popen instead of exec
4. ✅ **Reusable** - Same package for all your LangGraph projects
5. ✅ **Tested** - Comprehensive test coverage
6. ✅ **Type-safe** - Full TypeScript/Python type support

## Migration Guide

### Update analysis-workflow

1. Install the package:
```bash
cd analysis-workflow
npm install ../claude-langgraph-headless
```

2. Update imports in:
   - `src/nodes/analyzer.ts`
   - `src/nodes/question-generator.ts`
   - `src/nodes/summarizer.ts`

3. Replace:
```typescript
import { callClaudeHeadless } from "../utils/claude-headless.js";
```

With:
```typescript
import { ClaudeHeadlessExecutor } from '@anthropic/claude-langgraph-headless';

const executor = new ClaudeHeadlessExecutor({
  outputFormat: 'json',
  timeout: 180000,
  useSubscription: true,
});
```

4. Replace calls:
```typescript
// Old
const result = await callClaudeHeadless(formatted.system, formatted.user);

// New
const response = await executor.execute({
  systemPrompt: formatted.system,
  userPrompt: formatted.user,
});
const result = response.result;
```

## Example: Complete Node Conversion

**Before:**
```typescript
import { callClaudeHeadless } from "../utils/claude-headless.js";

export async function analyzeConversation(state: GraphStateType) {
  const result = await callClaudeHeadless(
    formatted.system,
    formatted.user
  );
  return { analysisResult: result };
}
```

**After:**
```typescript
import { ClaudeHeadlessExecutor } from '@anthropic/claude-langgraph-headless';

const executor = new ClaudeHeadlessExecutor({
  outputFormat: 'json',
  timeout: 180000,
  useSubscription: true,
});

export async function analyzeConversation(state: GraphStateType) {
  const response = await executor.execute({
    systemPrompt: formatted.system,
    userPrompt: formatted.user,
  });
  return { analysisResult: response.result };
}
```

This gives you all the robustness improvements with minimal code changes!
