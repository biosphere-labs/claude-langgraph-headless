# Claude Headless Subscription - TypeScript

TypeScript/JavaScript implementation for using Claude Code programmatically via your subscription.

## Installation

```bash
npm install claude-headless-subscription
```

## Quick Start

```typescript
import { ClaudeHeadlessNode } from 'claude-headless-subscription';

const claude = new ClaudeHeadlessNode({
  useSubscription: true,
  outputFormat: 'json'
});

const result = await claude.invoke({
  systemPrompt: "You are a helpful assistant.",
  userPrompt: "Analyze this data..."
});
```

## Development

```bash
npm install
npm run build
npm test
```

## Publishing

```bash
npm run build
npm publish
```

## Documentation

See the [main repository README](https://github.com/biosphere-labs/claude-headless-subscription) for full documentation.
