"""
Basic usage example - Python
"""

import asyncio
from claude_langgraph_headless import (
    ClaudeHeadlessExecutor,
    ClaudeHeadlessNode,
    ClaudeHeadlessOptions,
    ClaudeHeadlessInput,
)


async def basic_example():
    """Basic executor usage"""
    print("=== Basic Claude Headless Example ===\n")

    # Create executor
    executor = ClaudeHeadlessExecutor(
        ClaudeHeadlessOptions(
            output_format="json",
            timeout=60,
            use_subscription=True,
        )
    )

    # Execute
    result = await executor.execute(
        ClaudeHeadlessInput(
            system_prompt="You are a helpful assistant that analyzes conversations.",
            user_prompt="What are the top 3 reasons conversations fail?",
        )
    )

    print("Result:", result["result"])
    print("Exit code:", result["exit_code"])


async def langgraph_node_example():
    """LangGraph node usage"""
    print("\n=== LangGraph Node Example ===\n")

    # Create a LangGraph-compatible node
    claude_node = ClaudeHeadlessNode(
        ClaudeHeadlessOptions(
            output_format="json",
            timeout=60,
        )
    )

    # Use in your LangGraph workflow
    result = await claude_node.ainvoke(
        ClaudeHeadlessInput(
            system_prompt="You are an expert at identifying missing context.",
            user_prompt="Analyze this conversation and identify what information was missing...",
        )
    )

    print("Node result:", result)


def sync_example():
    """Synchronous usage"""
    print("\n=== Synchronous Example ===\n")

    node = ClaudeHeadlessNode(
        ClaudeHeadlessOptions(timeout=60)
    )

    # Synchronous invoke
    result = node.invoke(
        ClaudeHeadlessInput(
            system_prompt="You are a helpful assistant.",
            user_prompt="Say hello",
        )
    )

    print("Sync result:", result["result"])


# Run examples
async def main():
    try:
        await basic_example()
        await langgraph_node_example()
        sync_example()
    except Exception as error:
        print(f"Error: {error}")
        exit(1)


if __name__ == "__main__":
    asyncio.run(main())
