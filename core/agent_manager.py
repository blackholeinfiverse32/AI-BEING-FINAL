"""
AI Being Unified - Agent Manager
Orchestrates multiple AI agents from BHIV system
"""
import asyncio
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

@dataclass
class AgentResult:
    agent_name: str
    result: Any
    confidence: float
    execution_time: float

class AgentManager:
    def __init__(self):
        self.agents = {}
        self.active_sessions = {}
    
    def register_agent(self, name: str, agent_instance):
        """Register an agent for use"""
        self.agents[name] = agent_instance
    
    async def execute_agent(self, agent_name: str, task_data: Dict[str, Any]) -> AgentResult:
        """Execute a specific agent"""
        if agent_name not in self.agents:
            raise ValueError(f"Agent {agent_name} not registered")
        
        import time
        start_time = time.time()
        
        agent = self.agents[agent_name]
        result = await agent.process(task_data)
        
        execution_time = time.time() - start_time
        
        return AgentResult(
            agent_name=agent_name,
            result=result,
            confidence=getattr(result, 'confidence', 0.8),
            execution_time=execution_time
        )
    
    async def execute_multi_agent_workflow(self, workflow: List[str], task_data: Dict[str, Any]) -> List[AgentResult]:
        """Execute multiple agents in sequence"""
        results = []
        current_data = task_data.copy()
        
        for agent_name in workflow:
            result = await self.execute_agent(agent_name, current_data)
            results.append(result)
            
            # Pass result to next agent
            current_data['previous_result'] = result.result
            
        return results