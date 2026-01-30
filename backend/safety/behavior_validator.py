"""Behavior Validation for AI interactions"""
from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class BehaviorAnalysis:
    is_compliant: bool
    risk_score: float
    flags: List[str]
    behavior_type: str

class BehaviorValidator:
    def __init__(self):
        self.behavior_patterns = {
            'manipulation': ['trick', 'deceive', 'manipulate', 'fool'],
            'evasion': ['bypass', 'circumvent', 'avoid detection', 'hide'],
            'escalation': ['privilege', 'admin', 'root', 'sudo', 'elevated']
        }
    
    def analyze_behavior(self, user_input: str, context: Dict[str, Any] = None) -> BehaviorAnalysis:
        flags = []
        risk_score = 0.0
        behavior_type = "normal"
        
        input_lower = user_input.lower()
        
        # Check manipulation attempts
        for pattern in self.behavior_patterns['manipulation']:
            if pattern in input_lower:
                flags.append(f"Manipulation attempt: {pattern}")
                risk_score += 0.3
                behavior_type = "suspicious"
        
        # Check evasion attempts
        for pattern in self.behavior_patterns['evasion']:
            if pattern in input_lower:
                flags.append(f"Evasion attempt: {pattern}")
                risk_score += 0.4
                behavior_type = "suspicious"
        
        # Check privilege escalation
        for pattern in self.behavior_patterns['escalation']:
            if pattern in input_lower:
                flags.append(f"Escalation attempt: {pattern}")
                risk_score += 0.5
                behavior_type = "high_risk"
        
        is_compliant = risk_score < 0.5
        
        return BehaviorAnalysis(
            is_compliant=is_compliant,
            risk_score=min(1.0, risk_score),
            flags=flags,
            behavior_type=behavior_type
        )
    
    def validate_interaction_pattern(self, history: List[str]) -> Dict[str, Any]:
        total_risk = 0.0
        all_flags = []
        
        for interaction in history:
            analysis = self.analyze_behavior(interaction)
            total_risk += analysis.risk_score
            all_flags.extend(analysis.flags)
        
        avg_risk = total_risk / len(history) if history else 0.0
        
        return {
            'average_risk': avg_risk,
            'is_safe_pattern': avg_risk < 0.3,
            'total_flags': len(all_flags),
            'flags': all_flags
        }
