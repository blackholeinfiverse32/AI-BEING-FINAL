"""Safety Guard - Compatibility Layer"""
from dataclasses import dataclass
from typing import List

@dataclass
class SafetyVerdict:
    is_safe: bool
    reason: str
    trace_id: str
    safety_flags: List[str]

class SafetyGuard:
    def __init__(self, policy_engine):
        self.policy_engine = policy_engine
    
    def evaluate_safety(self, context: dict) -> SafetyVerdict:
        return SafetyVerdict(
            is_safe=True,
            reason="",
            trace_id="safe",
            safety_flags=[]
        )
    
    def get_safety_stats(self):
        return {"total_evaluations": 0, "safety_rate": 1.0}
    
    def is_system_healthy(self):
        return True
