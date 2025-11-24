"""Tests for Claude headless executor"""

import pytest
import subprocess
import asyncio
from claude_langgraph_headless import (
    ClaudeHeadlessExecutor,
    ClaudeHeadlessNode,
    ClaudeHeadlessOptions,
    ClaudeHeadlessInput,
)


def has_claude_cli() -> bool:
    """Check if Claude CLI is available"""
    try:
        result = subprocess.run(
            ["which", "claude"],
            capture_output=True,
            timeout=5
        )
        return result.returncode == 0
    except:
        return False


pytestmark = pytest.mark.skipif(
    not has_claude_cli(),
    reason="Claude CLI not available"
)


class TestClaudeHeadlessExecutor:
    """Test Claude headless executor"""

    @pytest.mark.asyncio
    @pytest.mark.timeout(70)
    async def test_simple_execution(self):
        """Test basic execution"""
        executor = ClaudeHeadlessExecutor(
            ClaudeHeadlessOptions(
                timeout=60,
                output_format="text"
            )
        )

        result = await executor.execute(
            ClaudeHeadlessInput(
                system_prompt="You are a helpful assistant. Respond with only 'OK'.",
                user_prompt="Say OK"
            )
        )

        assert result["result"]
        assert result["exit_code"] == 0

    @pytest.mark.asyncio
    @pytest.mark.timeout(70)
    async def test_json_output(self):
        """Test JSON output format"""
        executor = ClaudeHeadlessExecutor(
            ClaudeHeadlessOptions(
                timeout=60,
                output_format="json"
            )
        )

        result = await executor.execute(
            ClaudeHeadlessInput(
                system_prompt="You are a helpful assistant.",
                user_prompt="What is 2+2? Reply with just the number."
            )
        )

        assert result["result"]
        assert "type" in result["result"]

    @pytest.mark.asyncio
    @pytest.mark.timeout(15)
    async def test_timeout(self):
        """Test timeout handling"""
        executor = ClaudeHeadlessExecutor(
            ClaudeHeadlessOptions(timeout=1)  # 1 second
        )

        with pytest.raises(Exception, match="timed out"):
            await executor.execute(
                ClaudeHeadlessInput(
                    system_prompt="You are a helpful assistant.",
                    user_prompt="Write a very long essay..."
                )
            )

    def test_sync_execution(self):
        """Test synchronous wrapper"""
        executor = ClaudeHeadlessExecutor(
            ClaudeHeadlessOptions(
                timeout=60,
                output_format="text"
            )
        )

        result = executor.execute_sync(
            ClaudeHeadlessInput(
                system_prompt="You are a helpful assistant. Be brief.",
                user_prompt="Say hello"
            )
        )

        assert result["result"]

    @pytest.mark.asyncio
    @pytest.mark.timeout(100)
    async def test_large_prompt(self):
        """Test handling of large prompts"""
        executor = ClaudeHeadlessExecutor(
            ClaudeHeadlessOptions(timeout=90)
        )

        # 10KB prompt
        large_text = "x" * 10000

        result = await executor.execute(
            ClaudeHeadlessInput(
                system_prompt="You are a helpful assistant. Respond briefly.",
                user_prompt=f"Here is large text: {large_text}\n\nJust say 'received'."
            )
        )

        assert result["result"]


class TestClaudeHeadlessNode:
    """Test LangGraph node"""

    @pytest.mark.asyncio
    @pytest.mark.timeout(70)
    async def test_async_invoke(self):
        """Test async invoke method"""
        node = ClaudeHeadlessNode(
            ClaudeHeadlessOptions(
                timeout=60,
                output_format="json"
            )
        )

        result = await node.ainvoke(
            ClaudeHeadlessInput(
                system_prompt="You are a helpful assistant.",
                user_prompt="Say hello"
            )
        )

        assert result["result"]
        assert result["exit_code"] == 0

    @pytest.mark.timeout(70)
    def test_sync_invoke(self):
        """Test sync invoke method"""
        node = ClaudeHeadlessNode(
            ClaudeHeadlessOptions(
                timeout=60,
                output_format="text"
            )
        )

        result = node.invoke(
            ClaudeHeadlessInput(
                system_prompt="You are a helpful assistant.",
                user_prompt="Say hello"
            )
        )

        assert result["result"]


class TestConfiguration:
    """Test configuration options"""

    def test_default_options(self):
        """Test default configuration"""
        executor = ClaudeHeadlessExecutor()
        assert executor.options.output_format == "json"
        assert executor.options.timeout == 180
        assert executor.options.use_subscription is True

    def test_custom_options(self):
        """Test custom configuration"""
        options = ClaudeHeadlessOptions(
            output_format="text",
            timeout=5,
            max_buffer=1024,
            use_subscription=False,
            retries=3
        )
        executor = ClaudeHeadlessExecutor(options)
        assert executor.options.output_format == "text"
        assert executor.options.timeout == 5
        assert executor.options.retries == 3
