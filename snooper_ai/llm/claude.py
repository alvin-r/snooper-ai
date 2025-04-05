"""
Claude (Anthropic) LLM provider implementation.
"""
import os
from typing import Optional

import anthropic

from .base import LLMProvider


class ClaudeProvider(LLMProvider):
    """Claude (Anthropic) LLM provider implementation."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "claude-3-7-sonnet-latest"):
        """
        Initialize the Claude provider.
        
        Args:
            api_key: Anthropic API key. If not provided, will try to get from ANTHROPIC_API_KEY env var
            model: The Claude model to use
        """
        self.api_key = api_key or os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise ValueError(
                "Anthropic API key must be provided either through the api_key parameter "
                "or ANTHROPIC_API_KEY environment variable"
            )
        
        self.model = model
        self.client = anthropic.Anthropic(api_key=self.api_key)
        
    def analyze_trace(self, trace_output: str, user_query: str) -> str:
        """
        Analyze the trace output using Claude and return insights based on user query.
        
        Args:
            trace_output: The captured trace output from PySnooper
            user_query: The user's question about the code execution
            
        Returns:
            str: Claude's analysis and response
        """
        system_prompt = """You are an expert Python debugger analyzing execution traces.
        Your task is to help users understand what happened during code execution by analyzing
        the trace output from PySnooper. Focus on answering the user's specific question while
        providing relevant context from the trace."""
        
        user_message = f"""Here is the execution trace from PySnooper:

{trace_output}

User's question about the execution:
{user_query}

Please analyze the trace and answer the question, providing specific examples from the trace
where relevant."""

        response = self.client.messages.create(
            model=self.model,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}],
            max_tokens=4000,
        )
        
        return response.content[0].text 