"""Intelligence Engine - Orchestrates intelligence operations"""
from typing import Dict, Any
from .core import IntelligenceCore

class IntelligenceEngine:
    def __init__(self):
        self.core = IntelligenceCore()
        self.processing_modes = ['analytical', 'creative', 'logical', 'intuitive']
    
    def process(self, input_data: str, mode: str = 'analytical', context: Dict[str, Any] = None) -> Dict[str, Any]:
        if mode not in self.processing_modes:
            mode = 'analytical'
        
        reasoning_result = self.core.reason(input_data, context)
        
        return {
            'mode': mode,
            'conclusion': reasoning_result.conclusion,
            'confidence': reasoning_result.confidence,
            'reasoning_steps': reasoning_result.reasoning_steps,
            'evidence': reasoning_result.evidence,
            'processing_complete': True
        }
    
    def analyze_complexity(self, input_data: str) -> Dict[str, Any]:
        complexity_score = min(1.0, len(input_data) / 1000)
        
        if complexity_score < 0.3:
            complexity_level = 'simple'
        elif complexity_score < 0.7:
            complexity_level = 'moderate'
        else:
            complexity_level = 'complex'
        
        return {
            'complexity_level': complexity_level,
            'complexity_score': complexity_score,
            'recommended_mode': 'logical' if complexity_level == 'complex' else 'analytical'
        }
