"""Type definitions for Claude LangGraph Headless"""

from typing import TypedDict, Literal, Optional
from dataclasses import dataclass


class ClaudeHeadlessInput(TypedDict):
    """Input for Claude headless execution"""
    system_prompt: str
    user_prompt: str


class ClaudeHeadlessOutput(TypedDict):
    """Output from Claude headless execution"""
    result: str
    error: Optional[str]
    exit_code: Optional[int]


@dataclass
class ClaudeHeadlessOptions:
    """Configuration options for Claude headless execution"""
    output_format: Literal["text", "json", "stream-json"] = "json"
    timeout: int = 180  # seconds
    max_buffer: int = 10 * 1024 * 1024  # 10MB
    use_subscription: bool = True
    retries: int = 0
