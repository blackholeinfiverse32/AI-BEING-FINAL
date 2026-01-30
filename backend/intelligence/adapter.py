"""Intelligence Adapter - Bridges intelligence layer with other components"""
from typing import Dict, Any
from .engine import IntelligenceEngine

class IntelligenceAdapter:
    def __init__(self):
        self.engine = IntelligenceEngine()
    
    def adapt_for_agents(self, agent_input: Dict[str, Any]) -> Dict[str, Any]:
        input_text = agent_input.get('input', '')
        context = agent_input.get('context', {})
        
        complexity = self.engine.analyze_complexity(input_text)
        result = self.engine.process(input_text, complexity['recommended_mode'], context)
        
        return {
            'agent_ready': True,
            'processed_input': result['conclusion'],
            'confidence': result['confidence'],
            'complexity': complexity['complexity_level'],
            'metadata': {
                'reasoning_steps': len(result['reasoning_steps']),
                'evidence_count': len(result['evidence'])
            }
        }
    
    def adapt_for_llm(self, llm_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        result = self.engine.process(llm_input, 'analytical', context)
        
        return {
            'enhanced_prompt': f"{llm_input}\n\nContext: {result['conclusion']}",
            'confidence': result['confidence'],
            'reasoning_applied': True
        }
