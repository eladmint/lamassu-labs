#\!/usr/bin/env python3
"""
TrustWrapper Open Source Setup
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Basic requirements for open source version
requirements = [
    "numpy>=1.21.0",
    "requests>=2.28.0",
    "aiohttp>=3.8.0",
    "cryptography>=3.4.0",
    "pydantic>=1.10.0",
]

setup(
    name="trustwrapper",
    version="1.0.0",
    author="Lamassu Labs",
    author_email="opensource@lamassulabs.ai",
    description="Open source AI trust verification infrastructure",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/lamassu-labs/trustwrapper",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
<<<<<<< HEAD
        "Intended Audience :: Developers",
=======
        "Intended Audience :: Developers", 
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Security",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    license="Apache 2.0",
)
<<<<<<< HEAD
EOF < /dev/null
=======
EOF < /dev/null
>>>>>>> 175afbc51eef8fe475bbc42703bff3cf5a864752
