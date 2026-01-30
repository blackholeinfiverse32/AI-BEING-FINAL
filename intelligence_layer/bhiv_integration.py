"""
BHIV Intelligence Integration
Integrated from AI-ASSISTANT repository (blackholeinfiverse83-bit)
"""
from typing import Dict, Any

class BHIVReasoner:
    """BHIV Reasoning Engine - orchestrates multi-agent workflows"""
    
    async def run(self, query: str, context: Dict[str, Any], agents: Dict[str, Any], tools: Dict[str, Any]) -> Dict[str, Any]:
        """Execute multi-agent reasoning workflow"""
        steps = []
        
        # Planner creates execution plan
        plan = await agents["planner"].run(query, context)
        steps.append(plan)
        
        # Execute each step based on type
        for task in plan["output"]["steps"]:
            if task["type"] == "research":
                steps.append(await agents["researcher"].run(task, context))
            elif task["type"] == "analyze":
                steps.append(await agents["analyst"].run(task, context))
            elif task["type"] == "execute":
                steps.append(await agents["executor"].run(task, context))
        
        # Evaluator provides final assessment
        final = await agents["evaluator"].run(steps, context)
        return final
    
    def finalize(self, result: Dict[str, Any]) -> Any:
        """Finalize reasoning result"""
        return result.get("output", result)


class BHIVCore:
    """BHIV Core - Main processing engine"""
    
    def __init__(self, memory_manager, agents: Dict[str, Any], tools: Dict[str, Any], reasoner: BHIVReasoner):
        self.memory = memory_manager
        self.agents = agents
        self.tools = tools
        self.reasoner = reasoner
    
    async def process(self, input_data: Dict[str, Any]) -> Any:
        """Process input through BHIV reasoning pipeline"""
        user_id = input_data.get("user_id", "default")
        
        # Retrieve context from memory
        context = self.memory.get_context(user_id)
        
        # Run reasoning workflow
        reasoning_steps = await self.reasoner.run(
            input_data.get("query", ""),
            context,
            self.agents,
            self.tools
        )
        
        # Finalize result
        final = self.reasoner.finalize(reasoning_steps)
        
        # Update memory - use add_message for compatibility
        try:
            self.memory.add_message(
                user_id,
                "user",
                input_data.get("query", "")
            )
            self.memory.add_message(
                user_id,
                "assistant",
                str(final)
            )
        except AttributeError:
            # Fallback if add_message doesn't exist
            pass
        
        return final


# Factory function to create BHIV system
def create_bhiv_system(memory_manager, agents: Dict[str, Any], tools: Dict[str, Any]) -> BHIVCore:
    """Create and initialize BHIV system"""
    reasoner = BHIVReasoner()
    return BHIVCore(memory_manager, agents, tools, reasoner)
