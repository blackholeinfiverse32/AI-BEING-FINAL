"""Content Evaluator Module"""
from typing import Dict, Any

class ContentEvaluator:
    def __init__(self):
        self.content_rules = {
            'max_length': 10000,
            'min_length': 1,
            'allowed_types': ['text', 'json', 'markdown']
        }
    
    def evaluate(self, content: str, content_type: str = 'text') -> Dict[str, Any]:
        issues = []
        score = 1.0
        
        # Check length
        if len(content) > self.content_rules['max_length']:
            issues.append(f"Content exceeds maximum length of {self.content_rules['max_length']}")
            score -= 0.3
        
        if len(content) < self.content_rules['min_length']:
            issues.append("Content is too short")
            score -= 0.5
        
        # Check type
        if content_type not in self.content_rules['allowed_types']:
            issues.append(f"Content type '{content_type}' not allowed")
            score -= 0.4
        
        return {
            'is_valid': len(issues) == 0,
            'score': max(0.0, score),
            'issues': issues
        }
