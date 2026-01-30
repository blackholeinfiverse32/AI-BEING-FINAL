"""Policy Engine - Compatibility Layer"""

class PolicyEngine:
    def __init__(self):
        self.policies = {}
    
    def get_safe_response_template(self, reason: str) -> str:
        return f"I cannot process this request due to: {reason}"
    
    def get_violation_stats(self):
        return {"total_violations": 0}
