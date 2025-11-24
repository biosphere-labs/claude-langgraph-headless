from setuptools import setup, find_packages
import os

# Get the path to README.md
readme_path = os.path.join(os.path.dirname(__file__), "..", "README.md")
if os.path.exists(readme_path):
    with open(readme_path, "r", encoding="utf-8") as fh:
        long_description = fh.read()
else:
    long_description = "LangGraph node for calling Claude Code in headless mode"

setup(
    name="claude-langgraph-headless",
    version="1.0.0",
    author="",
    description="LangGraph node for calling Claude Code in headless mode",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/biosphere-labs/claude-langgraph-headless",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
    ],
    python_requires=">=3.8",
    install_requires=[],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "pytest-timeout>=2.1.0",
        ],
    },
)
