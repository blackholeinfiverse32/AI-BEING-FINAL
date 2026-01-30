"""Enforcement Gateway - Entry point for all enforcement checks"""
from typing import Dict, Any
from .enforcement_engine import EnforcementEngine

class EnforcementGateway:
    def __init__(self):
        self.engine = EnforcementEngine()
        self.request_count = {}
    
    def check_request(self, user_id: str, request_data: Dict[str, Any]) -> Dict[str, Any]:
        # Build enforcement context
        context = {
            'user_id': user_id,
            'request_data': request_data,
            'harmful_detected': self._check_harmful(request_data),
            'rate_exceeded': self._check_rate_limit(user_id),
            'sensitive_data': self._check_sensitive_data(request_data),
            'injection_detected': self._check_injection(request_data),
            'suspicious_behavior': self._check_behavior(user_id, request_data)
        }
        
        # Evaluate with enforcement engine
        result = self.engine.evaluate(context)
        
        # Update request count
        self._update_rate_limit(user_id)
        
        return {
            'allowed': result['action'] in ['allow', 'warn'],
            'action': result['action'],
            'severity': result['severity'],
            'rules_triggered': result['triggered_rules'],
            'message': self._get_message(result['action'])
        }
    
    def _check_harmful(self, data: Dict[str, Any]) -> bool:
        content = str(data.get('message', '')).lower()
        harmful_keywords = ['harm', 'kill', 'destroy', 'attack', 'bomb']
        return any(keyword in content for keyword in harmful_keywords)
    
    def _check_rate_limit(self, user_id: str) -> bool:
        count = self.request_count.get(user_id, 0)
        return count > 100  # 100 requests threshold
    
    def _check_sensitive_data(self, data: Dict[str, Any]) -> bool:
        content = str(data.get('message', '')).lower()
        sensitive = ['password', 'credit card', 'ssn', 'api key']
        return any(term in content for term in sensitive)
    
    def _check_injection(self, data: Dict[str, Any]) -> bool:
        content = str(data.get('message', ''))
        injection_patterns = ['<script', 'DROP TABLE', 'exec(', 'eval(']
        return any(pattern in content for pattern in injection_patterns)
    
    def _check_behavior(self, user_id: str, data: Dict[str, Any]) -> bool:
        # Simple behavior check
        return False  # Placeholder
    
    def _update_rate_limit(self, user_id: str):
        self.request_count[user_id] = self.request_count.get(user_id, 0) + 1
    
    def _get_message(self, action: str) -> str:
        messages = {
            'block': 'Request blocked due to policy violation',
            'throttle': 'Request throttled due to rate limiting',
            'redact': 'Sensitive data detected and redacted',
            'warn': 'Request allowed with warning',
            'allow': 'Request allowed'
        }
        return messages.get(action, 'Unknown action')
