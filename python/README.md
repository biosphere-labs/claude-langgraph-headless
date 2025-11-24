# Claude Headless Subscription - Python

Python implementation for using Claude Code programmatically via your subscription.

## Installation

```bash
pip install claude-headless-subscription
```

## Quick Start

```python
from claude_headless_subscription import ClaudeHeadlessNode, ClaudeHeadlessOptions, ClaudeHeadlessInput

claude = ClaudeHeadlessNode(
    ClaudeHeadlessOptions(
        use_subscription=True,
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

## Development

```bash
pip install -e ".[dev]"
pytest
```

## Publishing

```bash
python setup.py sdist bdist_wheel
twine upload dist/*
```

## Documentation

See the [main repository README](https://github.com/biosphere-labs/claude-headless-subscription) for full documentation.
