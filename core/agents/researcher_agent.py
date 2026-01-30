"""Researcher Agent - Gathers information using search and LLM"""
from typing import Dict, Any
from .base_agent import BaseAgent

class ResearcherAgent(BaseAgent):
    """Agent that researches and gathers information"""
    name = "researcher"
    
    async def run(self, query: Any, context: Dict[str, Any]) -> Dict[str, Any]:
        """Gather information from query"""
        info = f"Gathered information from query: {str(query)}"
        return {"agent": self.name, "output": info}
