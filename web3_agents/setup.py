from setuptools import find_packages, setup

setup(
    name="nuru-ai-web3-agents",
    version="2.0.0",
    packages=find_packages(),
    install_requires=[
        "web3>=6.0.0",
        "wasmtime>=20.0.0",
        "httpx>=0.27.0",
        "pydantic>=2.8.0",
        "python-dotenv>=1.0.0",
        "anyio>=1.4.0",
        "python-dateutil>=2.9.0",
        "pytz>=2024.1",
        "redis>=5.0.0",
        "supabase>=1.0.0",
        "fastapi>=0.100.0",
        "uvicorn[standard]>=0.29.0",
    ],
    entry_points={
        "console_scripts": [
            "nuru-web3-agents=web3_agents.main:main",
        ],
    },
    python_requires=">=3.10",
    description="Nuru AI Web3 Agents Service - AI agents for Web3 ecosystem interactions",
    author="Nuru AI Team",
    license="MIT",
)
