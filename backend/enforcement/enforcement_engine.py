"""Enhanced Enforcement Engine"""
from typing import Dict, Any, List
from dataclasses import dataclass
from datetime import datetime

@dataclass
class EnforcementRule:
    rule_id: str
    name: str
    condition: str
    action: str
    severity: str
    enabled: bool = True

class EnforcementEngine:
    def __init__(self):
        self.rules = self._load_default_rules()
        self.violation_log = []
    
    def _load_default_rules(self) -> List[EnforcementRule]:
        return [
            EnforcementRule("R001", "Block Harmful Content", "harmful_detected", "block", "critical"),
            EnforcementRule("R002", "Rate Limiting", "rate_exceeded", "throttle", "medium"),
            EnforcementRule("R003", "Sensitive Data Protection", "sensitive_data", "redact", "high"),
            EnforcementRule("R004", "Injection Prevention", "injection_detected", "block", "critical"),
            EnforcementRule("R005", "Behavior Monitoring", "suspicious_behavior", "warn", "medium")
        ]
    
    def evaluate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        triggered_rules = []
        actions = []
        
        for rule in self.rules:
            if not rule.enabled:
                continue
            
            if self._check_condition(rule.condition, context):
                triggered_rules.append(rule)
                actions.append(rule.action)
        
        # Determine final action
        if 'block' in actions:
            final_action = 'block'
        elif 'throttle' in actions:
            final_action = 'throttle'
        elif 'redact' in actions:
            final_action = 'redact'
        elif 'warn' in actions:
            final_action = 'warn'
        else:
            final_action = 'allow'
        
        # Log violation
        if triggered_rules:
            self._log_violation(triggered_rules, context)
        
        return {
            'action': final_action,
            'triggered_rules': [r.rule_id for r in triggered_rules],
            'severity': max([r.severity for r in triggered_rules], default='low', 
                          key=lambda x: ['low', 'medium', 'high', 'critical'].index(x)),
            'timestamp': datetime.now().isoformat()
        }
    
    def _check_condition(self, condition: str, context: Dict[str, Any]) -> bool:
        # Simple condition checking
        return context.get(condition, False)
    
    def _log_violation(self, rules: List[EnforcementRule], context: Dict[str, Any]):
        self.violation_log.append({
            'timestamp': datetime.now().isoformat(),
            'rules': [r.rule_id for r in rules],
            'context': context
        })
    
    def get_violation_stats(self) -> Dict[str, Any]:
        return {
            'total_violations': len(self.violation_log),
            'recent_violations': self.violation_log[-10:],
            'rules_triggered': len(set(r for log in self.violation_log for r in log['rules']))
        }
