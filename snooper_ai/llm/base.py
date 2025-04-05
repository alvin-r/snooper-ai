"""
Base class for LLM providers.
"""
from abc import ABC, abstractmethod
from typing import List, Optional


class LLMProvider(ABC):
    """Base class for LLM providers."""
    
    @abstractmethod
    def analyze_trace(self, trace_output: str, user_query: str) -> str:
        """
        Analyze the trace output using the LLM and return insights based on user query.
        
        Args:
            trace_output: The captured trace output from PySnooper
            user_query: The user's question about the code execution
            
        Returns:
            str: The LLM's analysis and response
        """
        pass 