"""Claude Code headless executor using robust subprocess management"""

import subprocess
import tempfile
import os
import time
from pathlib import Path
from typing import Optional
import asyncio

from .types import ClaudeHeadlessInput, ClaudeHeadlessOutput, ClaudeHeadlessOptions


class ClaudeHeadlessExecutor:
    """Robust Claude Code headless executor using Popen for better process control"""

    def __init__(self, options: Optional[ClaudeHeadlessOptions] = None):
        self.options = options or ClaudeHeadlessOptions()

    async def execute(self, input_data: ClaudeHeadlessInput) -> ClaudeHeadlessOutput:
        """Execute Claude Code in headless mode with retries"""
        attempt = 0
        last_error: Optional[Exception] = None

        while attempt <= self.options.retries:
            try:
                return await self._execute_once(input_data)
            except Exception as error:
                last_error = error
                attempt += 1
                if attempt <= self.options.retries:
                    print(f"Attempt {attempt} failed, retrying...")
                    await asyncio.sleep(attempt)  # Exponential backoff

        raise last_error or Exception("Execution failed")

    async def _execute_once(self, input_data: ClaudeHeadlessInput) -> ClaudeHeadlessOutput:
        """Execute Claude Code once"""
        # Create temp file for prompt
        with tempfile.NamedTemporaryFile(
            mode='w',
            suffix='.txt',
            delete=False,
            encoding='utf-8'
        ) as temp_file:
            temp_path = temp_file.name
            full_prompt = f"{input_data['system_prompt']}\n\n---\n\n{input_data['user_prompt']}"
            temp_file.write(full_prompt)

        try:
            result = await self._spawn_claude_process(temp_path)
            return result
        finally:
            # Clean up temp file
            try:
                os.unlink(temp_path)
            except:
                pass

    async def _spawn_claude_process(self, temp_path: str) -> ClaudeHeadlessOutput:
        """Spawn Claude process using Popen for better control"""

        # Build command
        args = ["claude", "-p", "--output-format", self.options.output_format]

        # Set up environment
        env = os.environ.copy()
        if self.options.use_subscription:
            # Remove API key to use subscription
            env.pop("ANTHROPIC_API_KEY", None)

        # Spawn process
        try:
            # Use cat to pipe file to claude stdin
            cat_proc = subprocess.Popen(
                ["cat", temp_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )

            claude_proc = subprocess.Popen(
                args,
                stdin=cat_proc.stdout,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                env=env
            )

            # Close cat stdout in parent to allow cat to receive SIGPIPE if claude exits
            if cat_proc.stdout:
                cat_proc.stdout.close()

            # Wait for completion with timeout
            try:
                stdout, stderr = await asyncio.wait_for(
                    asyncio.create_task(
                        asyncio.to_thread(claude_proc.communicate)
                    ),
                    timeout=self.options.timeout
                )
            except asyncio.TimeoutError:
                claude_proc.kill()
                cat_proc.kill()
                raise TimeoutError(
                    f"Claude process timed out after {self.options.timeout} seconds"
                )

            # Check result
            stdout_str = stdout.decode('utf-8', errors='replace')
            stderr_str = stderr.decode('utf-8', errors='replace')

            # Check for credit balance error
            if "Credit balance is too low" in stdout_str:
                raise Exception(
                    "Credit balance is too low. Use subscription authentication or add API credits."
                )

            if claude_proc.returncode != 0:
                raise Exception(
                    f"Claude process exited with code {claude_proc.returncode}\n"
                    f"Stderr: {stderr_str}\n"
                    f"Stdout: {stdout_str}"
                )

            return ClaudeHeadlessOutput(
                result=stdout_str.strip(),
                error=None,
                exit_code=claude_proc.returncode
            )

        except FileNotFoundError:
            raise Exception(
                "Claude CLI not found. Make sure Claude Code is installed and in PATH."
            )
        except Exception as e:
            raise Exception(f"Failed to execute Claude: {str(e)}")

    def execute_sync(self, input_data: ClaudeHeadlessInput) -> ClaudeHeadlessOutput:
        """Synchronous execute wrapper"""
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # Already in an event loop, use run_until_complete
                return loop.run_until_complete(self.execute(input_data))
            else:
                return asyncio.run(self.execute(input_data))
        except RuntimeError:
            # No event loop, create new one
            return asyncio.run(self.execute(input_data))


class ClaudeHeadlessNode:
    """LangGraph-compatible node for Claude Code headless execution"""

    def __init__(self, options: Optional[ClaudeHeadlessOptions] = None):
        self.executor = ClaudeHeadlessExecutor(options)

    async def ainvoke(self, input_data: ClaudeHeadlessInput) -> ClaudeHeadlessOutput:
        """Async LangGraph node invoke method"""
        return await self.executor.execute(input_data)

    def invoke(self, input_data: ClaudeHeadlessInput) -> ClaudeHeadlessOutput:
        """Sync LangGraph node invoke method"""
        return self.executor.execute_sync(input_data)
