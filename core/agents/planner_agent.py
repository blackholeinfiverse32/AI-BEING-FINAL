"""Planner Agent - Breaks down tasks into executable steps"""
from typing import Dict, Any
from .base_agent import BaseAgent

class PlannerAgent(BaseAgent):
    """Agent that plans task execution by breaking down into steps"""
    name = "planner"
    
    async def run(self, query: Any, context: Dict[str, Any]) -> Dict[str, Any]:
        """Break query into executable steps"""
        steps = [
            {"type": "research", "description": "Gather information"},
            {"type": "analyze", "description": "Analyze data"},
            {"type": "execute", "description": "Execute actions"},
        ]
        return {"agent": self.name, "output": {"steps": steps}}
