"""Unified Safety Validator"""
from typing import Dict, Any, List
from dataclasses import dataclass
from enum import Enum

class SafetyLevel(Enum):
    SAFE = "safe"
    CAUTION = "caution"
    DANGER = "danger"
    CRITICAL = "critical"

@dataclass
class ValidationResult:
    is_safe: bool
    level: SafetyLevel
    violations: List[str]
    score: float
    recommendations: List[str]

class UnifiedValidator:
    def __init__(self):
        self.patterns = {
            'harmful': ['harm', 'kill', 'destroy', 'attack', 'weapon', 'bomb', 'exploit'],
            'sensitive': ['password', 'credit card', 'ssn', 'private key', 'secret'],
            'inappropriate': ['hate', 'discriminate', 'abuse', 'harass']
        }
    
    def validate(self, content: str, context: Dict[str, Any] = None) -> ValidationResult:
        violations = []
        score = 1.0
        level = SafetyLevel.SAFE
        
        content_lower = content.lower()
        
        # Check harmful patterns
        for pattern in self.patterns['harmful']:
            if pattern in content_lower:
                violations.append(f"Harmful content detected: {pattern}")
                score -= 0.3
                level = SafetyLevel.DANGER
        
        # Check sensitive data
        for pattern in self.patterns['sensitive']:
            if pattern in content_lower:
                violations.append(f"Sensitive data detected: {pattern}")
                score -= 0.2
                if level == SafetyLevel.SAFE:
                    level = SafetyLevel.CAUTION
        
        # Check inappropriate content
        for pattern in self.patterns['inappropriate']:
            if pattern in content_lower:
                violations.append(f"Inappropriate content: {pattern}")
                score -= 0.25
                if level == SafetyLevel.SAFE:
                    level = SafetyLevel.CAUTION
        
        score = max(0.0, score)
        is_safe = score >= 0.5 and level in [SafetyLevel.SAFE, SafetyLevel.CAUTION]
        
        recommendations = []
        if not is_safe:
            recommendations.append("Rephrase content to remove harmful elements")
            recommendations.append("Review content policy guidelines")
        
        return ValidationResult(
            is_safe=is_safe,
            level=level,
            violations=violations,
            score=score,
            recommendations=recommendations
        )
    
    def validate_batch(self, contents: List[str]) -> List[ValidationResult]:
        return [self.validate(content) for content in contents]
