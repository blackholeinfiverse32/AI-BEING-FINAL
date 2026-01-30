"""Risk Evaluator Module"""
from typing import Dict, Any, List

class RiskEvaluator:
    def __init__(self):
        self.risk_factors = {
            'high_risk_keywords': ['exploit', 'vulnerability', 'bypass', 'hack'],
            'medium_risk_keywords': ['access', 'permission', 'credential'],
            'low_risk_keywords': ['test', 'debug', 'sample']
        }
    
    def evaluate_risk(self, content: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        risk_level = 'low'
        risk_score = 0.0
        factors = []
        
        content_lower = content.lower()
        
        # Check high risk
        for keyword in self.risk_factors['high_risk_keywords']:
            if keyword in content_lower:
                factors.append(f"High risk keyword: {keyword}")
                risk_score += 0.4
                risk_level = 'high'
        
        # Check medium risk
        for keyword in self.risk_factors['medium_risk_keywords']:
            if keyword in content_lower:
                factors.append(f"Medium risk keyword: {keyword}")
                risk_score += 0.2
                if risk_level == 'low':
                    risk_level = 'medium'
        
        # Check low risk
        for keyword in self.risk_factors['low_risk_keywords']:
            if keyword in content_lower:
                factors.append(f"Low risk keyword: {keyword}")
                risk_score += 0.1
        
        risk_score = min(1.0, risk_score)
        
        return {
            'risk_level': risk_level,
            'risk_score': risk_score,
            'factors': factors,
            'requires_review': risk_score > 0.5
        }
