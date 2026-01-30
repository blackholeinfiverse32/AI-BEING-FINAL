"""Base Agent for specialized agent implementations"""
from typing import Dict, Any

class BaseAgent:
    """Base class for all specialized agents"""
    name = "base"
    
    async def run(self, query: Any, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute agent logic"""
        return {"agent": self.name, "output": "not implemented"}
