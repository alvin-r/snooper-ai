"""
OpenAI LLM provider implementation.
"""
import os
from typing import Optional

from openai import OpenAI

from .base import LLMProvider


class OpenAIProvider(LLMProvider):
    """OpenAI LLM provider implementation."""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o"):
        """
        Initialize the OpenAI provider.
        
        Args:
            api_key: OpenAI API key. If not provided, will try to get from OPENAI_API_KEY env var
            model: The OpenAI model to use
        """
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError(
                "OpenAI API key must be provided either through the api_key parameter "
                "or OPENAI_API_KEY environment variable"
            )
        
        self.model = model
        self.client = OpenAI(api_key=self.api_key)
        
    def analyze_trace(self, trace_output: str, user_query: str) -> str:
        """
        Analyze the trace output using OpenAI and return insights based on user query.
        
        Args:
            trace_output: The captured trace output from PySnooper
            user_query: The user's question about the code execution
            
        Returns:
            str: OpenAI's analysis and response
        """
        system_prompt = """You are an expert Python debugger analyzing execution traces.
        Your task is to help users understand what happened during code execution by analyzing
        the trace output from PySnooper. Focus on answering the user's specific question while
        providing relevant context from the trace."""
        
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"""Here is the execution trace from PySnooper:

{trace_output}

User's question about the execution:
{user_query}

Please analyze the trace and answer the question, providing specific examples from the trace
where relevant."""}
            ],
            max_tokens=4000,
        )
        
        return response.choices[0].message.content 