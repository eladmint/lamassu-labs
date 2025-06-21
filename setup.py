"""
Setup script for Lamassu Labs

Install with: pip install -e .
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="lamassu-labs",
    version="0.1.0",
    description="ZK-Powered AI Agent Marketplace - Privacy-preserving AI agent verification using Aleo",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Lamassu Labs Team",
    author_email="team@lamassu-labs.dev",
    url="https://github.com/eladmint/lamassu-labs",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "aiohttp>=3.8.0",
        "playwright>=1.40.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=23.0.0",
            "ruff>=0.1.0",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Security :: Cryptography",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    keywords="zero-knowledge, ai-agents, blockchain, aleo, privacy",
)