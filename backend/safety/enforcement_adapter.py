"""Enforcement Adapter - Bridges safety validators with enforcement engine"""
from typing import Dict, Any
from .unified_validator import UnifiedValidator
from .behavior_validator import BehaviorValidator
from .hardened_validator import HardenedValidator

class EnforcementAdapter:
    def __init__(self):
        self.unified_validator = UnifiedValidator()
        self.behavior_validator = BehaviorValidator()
        self.hardened_validator = HardenedValidator()
    
    def comprehensive_check(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        # Run all validators
        unified_result = self.unified_validator.validate(user_input, context)
        behavior_result = self.behavior_validator.analyze_behavior(user_input, context)
        hardened_result = self.hardened_validator.validate_input(user_input)
        
        # Aggregate results
        is_safe = (
            unified_result.is_safe and
            behavior_result.is_compliant and
            hardened_result['is_safe']
        )
        
        all_violations = []
        all_violations.extend(unified_result.violations)
        all_violations.extend(behavior_result.flags)
        all_violations.extend(hardened_result['threats'])
        
        risk_score = (
            (1.0 - unified_result.score) * 0.4 +
            behavior_result.risk_score * 0.3 +
            (0.0 if hardened_result['is_safe'] else 1.0) * 0.3
        )
        
        return {
            'is_safe': is_safe,
            'risk_score': risk_score,
            'violations': all_violations,
            'safety_level': unified_result.level.value,
            'behavior_type': behavior_result.behavior_type,
            'security_severity': hardened_result['severity'],
            'recommendations': unified_result.recommendations,
            'action': 'allow' if is_safe else 'block'
        }
    
    def validate_and_enforce(self, user_input: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        result = self.comprehensive_check(user_input, context)
        
        # Add enforcement actions
        if not result['is_safe']:
            result['enforcement_action'] = {
                'block': True,
                'log': True,
                'alert': result['risk_score'] > 0.7,
                'quarantine': result['security_severity'] == 'critical'
            }
        else:
            result['enforcement_action'] = {
                'block': False,
                'log': True,
                'alert': False,
                'quarantine': False
            }
        
        return result
