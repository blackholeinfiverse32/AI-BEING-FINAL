"""Analyst Agent - Analyzes data and provides insights"""
from typing import Dict, Any
from .base_agent import BaseAgent

class AnalystAgent(BaseAgent):
    """Agent that analyzes data and provides insights"""
    name = "analyst"
    
    async def run(self, query: Any, context: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze data from query"""
        analysis = f"Analysis of: {str(query)}"
        return {"agent": self.name, "output": analysis}
