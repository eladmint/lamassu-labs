"""
Base types for TrustWrapper LangChain integration.

These mirror LangChain types to allow the integration to work
without requiring LangChain to be installed.
"""

from typing import Any, Dict, List


class BaseCallbackHandler:
    """Base callback handler interface (mirrors LangChain)"""

    async def on_llm_start(
        self, serialized: Dict[str, Any], prompts: List[str], **kwargs: Any
    ) -> None:
        """Called when LLM starts"""
        pass

    async def on_llm_end(self, response: Any, **kwargs: Any) -> None:
        """Called when LLM ends"""
        pass

    async def on_tool_start(
        self, serialized: Dict[str, Any], input_str: str, **kwargs: Any
    ) -> None:
        """Called when tool starts"""
        pass

    async def on_tool_end(self, output: str, **kwargs: Any) -> None:
        """Called when tool ends"""
        pass

    async def on_agent_action(self, action: Any, **kwargs: Any) -> None:
        """Called on agent action"""
        pass

    async def on_agent_finish(self, finish: Any, **kwargs: Any) -> None:
        """Called when agent finishes"""
        pass

    async def on_chain_error(self, error: Exception, **kwargs: Any) -> None:
        """Called on chain error"""
        pass


class AsyncCallbackHandler(BaseCallbackHandler):
    """Async callback handler (mirrors LangChain)"""

    pass


class LLMResult:
    """LLM result container (mirrors LangChain)"""

    def __init__(self, generations: List[List[Any]]):
        self.generations = generations


class AgentAction:
    """Agent action (mirrors LangChain)"""

    def __init__(self, tool: str, tool_input: Any, log: str):
        self.tool = tool
        self.tool_input = tool_input
        self.log = log


class AgentFinish:
    """Agent finish (mirrors LangChain)"""

    def __init__(self, return_values: Dict[str, Any], log: str):
        self.return_values = return_values
        self.log = log
