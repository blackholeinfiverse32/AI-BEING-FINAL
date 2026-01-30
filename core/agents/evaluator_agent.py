"""Evaluator Agent - Evaluates results and provides final assessment"""
from typing import Dict, Any, List
from .base_agent import BaseAgent

class EvaluatorAgent(BaseAgent):
    """Agent that evaluates results and provides final assessment"""
    name = "evaluator"
    
    async def run(self, steps: List[Dict[str, Any]], context: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate execution steps and provide final result"""
        evaluation = f"Evaluated {len(steps)} steps"
        return {"agent": self.name, "output": evaluation}
