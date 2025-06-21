"""
Setup script for Lamassu Labs

Install with: pip install -e .
"""

from setuptools import setup, find_packages

setup(
    name="lamassu-labs",
    version="0.1.0",
    description="ZK-Powered AI Agent Marketplace for ZK-Berlin Hackathon",
    author="Nuru AI Team",
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.8.0",
        "playwright>=1.40.0",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)