#!/usr/bin/env python3
"""
Simple test to verify the Python package works
"""

import sys
import asyncio
sys.path.insert(0, 'python')

from claude_langgraph_headless import (
    ClaudeHeadlessNode,
    ClaudeHeadlessOptions,
    ClaudeHeadlessInput,
)


async def test_async():
    """Test async invoke"""
    print('Testing Claude Headless Node (Python - Async)...\n')

    node = ClaudeHeadlessNode(
        ClaudeHeadlessOptions(
            output_format='text',
            timeout=60,
            use_subscription=True,
        )
    )

    try:
        result = await node.ainvoke(
            ClaudeHeadlessInput(
                system_prompt='You are a helpful assistant. Respond with only "WORKING".',
                user_prompt='Test message - respond with WORKING',
            )
        )

        print('✅ Async Success!')
        print('Result:', result['result'])
        print('Exit code:', result['exit_code'])
        return True
    except Exception as error:
        print(f'❌ Error: {error}')
        return False


def test_sync():
    """Test sync invoke"""
    print('\nTesting Claude Headless Node (Python - Sync)...\n')

    node = ClaudeHeadlessNode(
        ClaudeHeadlessOptions(
            output_format='text',
            timeout=60,
            use_subscription=True,
        )
    )

    try:
        result = node.invoke(
            ClaudeHeadlessInput(
                system_prompt='You are a helpful assistant. Respond with only "WORKING".',
                user_prompt='Test message - respond with WORKING',
            )
        )

        print('✅ Sync Success!')
        print('Result:', result['result'])
        print('Exit code:', result['exit_code'])
        return True
    except Exception as error:
        print(f'❌ Error: {error}')
        return False


def main():
    # Test async version
    async_ok = asyncio.run(test_async())

    # Test sync version (call from non-async context)
    sync_ok = test_sync()

    if async_ok and sync_ok:
        print('\n🎉 All Python tests passed!')
        sys.exit(0)
    else:
        print('\n❌ Some tests failed')
        sys.exit(1)


if __name__ == '__main__':
    main()
