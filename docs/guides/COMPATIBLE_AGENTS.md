# 🔌 TrustWrapper Compatible Agents & Libraries

TrustWrapper can wrap **ANY** Python code that has methods. Here's a comprehensive list of what you can wrap:

## 🌐 Web Scraping & Browser Automation

### Production Ready
- **Playwright** - Modern browser automation
  ```python
  from playwright.sync_api import sync_playwright
  trusted_browser = ZKTrustWrapper(PlaywrightAgent())
  ```

- **Selenium** - Classic web automation
  ```python
  from selenium import webdriver
  trusted_selenium = ZKTrustWrapper(SeleniumBot())
  ```

- **BeautifulSoup** - HTML parsing
  ```python
  from bs4 import BeautifulSoup
  trusted_parser = ZKTrustWrapper(SoupParser())
  ```

- **Scrapy** - Web scraping framework
  ```python
  trusted_spider = ZKTrustWrapper(ScrapySpider())
  ```

## 🤖 AI & LLM Agents

### OpenAI Compatible
- **OpenAI GPT** - ChatGPT, GPT-4
  ```python
  trusted_gpt = ZKTrustWrapper(GPTAgent())
  ```

- **Anthropic Claude** - Claude API
  ```python
  trusted_claude = ZKTrustWrapper(ClaudeAgent())
  ```

- **LangChain** - Any LangChain agent
  ```python
  from langchain.agents import create_react_agent
  trusted_langchain = ZKTrustWrapper(LangChainWrapper(agent))
  ```

- **LlamaIndex** - Data framework agents
  ```python
  trusted_llama = ZKTrustWrapper(LlamaIndexAgent())
  ```

## 🔗 Blockchain & DeFi

### Web3 Libraries
- **Web3.py** - Ethereum interactions
  ```python
  from web3 import Web3
  trusted_web3 = ZKTrustWrapper(Web3Agent())
  ```

- **Ethers.py** - Ethereum library
  ```python
  trusted_ethers = ZKTrustWrapper(EthersAgent())
  ```

- **CCXT** - Crypto exchange trading
  ```python
  import ccxt
  trusted_trader = ZKTrustWrapper(TradingBot())
  ```

## 📊 Data Processing

### Analytics Libraries
- **Pandas** - Data analysis
  ```python
  import pandas as pd
  trusted_analyzer = ZKTrustWrapper(PandasAnalyzer())
  ```

- **NumPy** - Numerical computing
  ```python
  import numpy as np
  trusted_compute = ZKTrustWrapper(NumpyProcessor())
  ```

- **Scikit-learn** - ML models
  ```python
  from sklearn import model
  trusted_ml = ZKTrustWrapper(MLPredictor())
  ```

## 🌐 HTTP & API Clients

### HTTP Libraries
- **Requests** - HTTP library
  ```python
  import requests
  trusted_http = ZKTrustWrapper(RequestsAgent())
  ```

- **HTTPX** - Async HTTP
  ```python
  import httpx
  trusted_async = ZKTrustWrapper(HTTPXAgent())
  ```

- **aiohttp** - Async HTTP client/server
  ```python
  import aiohttp
  trusted_aio = ZKTrustWrapper(AIOHTTPAgent())
  ```

## 🏢 Enterprise Frameworks

### From Nuru AI
- **EventDataExtractorAgent** - Web3 event extraction
- **AdvancedVisualIntelligenceAgent** - Image analysis
- **DataCompilerAgent** - Data compilation
- **LinkFinderAgent** - Link discovery

### From Agent Forge
- **AsyncContextAgent** - Async operations
- **ExplainableAgent** - AI with explanations
- **MCPEnabledAgent** - MCP protocol agents
- **ValidationAgent** - Data validation

## 🛠️ Custom Agents

### Any Custom Code
```python
# Database clients
class DatabaseAgent:
    def query(self, sql): 
        return results

trusted_db = ZKTrustWrapper(DatabaseAgent())

# Trading bots
class TradingBot:
    def analyze(self, market_data):
        return signals

trusted_trader = ZKTrustWrapper(TradingBot())

# Monitoring tools
class MonitoringAgent:
    def check_health(self, service):
        return status

trusted_monitor = ZKTrustWrapper(MonitoringAgent())
```

## 🔑 Key Requirements

The ONLY requirement is that your code has callable methods:

```python
# ✅ Works - has methods
class MyAgent:
    def execute(self): pass
    def run(self): pass
    def process(self): pass

# ✅ Works - any callable
class MyTool:
    def do_something(self): pass

# ❌ Doesn't work - no methods
class JustData:
    data = [1, 2, 3]
```

## 🎯 Common Use Cases

### API Monitoring
- Prove SLA compliance without revealing endpoints
- Verify response times with cryptographic proof
- Track availability without exposing infrastructure

### Web Scraping
- Prove data freshness without revealing sources
- Verify extraction success without showing methods
- Demonstrate compliance without exposing targets

### DeFi Bots
- Prove trading performance without strategies
- Verify liquidity monitoring without addresses
- Show profits without revealing alpha

### AI Agents
- Prove model accuracy without prompts
- Verify AI decisions without training data
- Demonstrate safety without implementation

### Data Processing
- Prove analysis quality without data
- Verify computations without inputs
- Show insights without exposure

## 🚀 Getting Started

```python
# 1. Import TrustWrapper
from trustwrapper import ZKTrustWrapper

# 2. Wrap ANY agent or code
trusted_agent = ZKTrustWrapper(your_agent)

# 3. Use normally - now with ZK proofs!
result = trusted_agent.execute()
```

**Remember**: If it has methods, it can be wrapped! 🛡️