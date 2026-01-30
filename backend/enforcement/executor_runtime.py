"""Executor Runtime - Manages execution of enforcement actions"""
from typing import Dict, Any, Callable
from datetime import datetime

class ExecutorRuntime:
    def __init__(self):
        self.action_handlers = {
            'block': self._handle_block,
            'throttle': self._handle_throttle,
            'redact': self._handle_redact,
            'warn': self._handle_warn,
            'allow': self._handle_allow
        }
        self.execution_log = []
    
    def execute(self, action: str, context: Dict[str, Any]) -> Dict[str, Any]:
        handler = self.action_handlers.get(action, self._handle_unknown)
        result = handler(context)
        
        # Log execution
        self._log_execution(action, context, result)
        
        return result
    
    def _handle_block(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'status': 'blocked',
            'message': 'Request blocked by enforcement policy',
            'allow_retry': False,
            'response': None
        }
    
    def _handle_throttle(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'status': 'throttled',
            'message': 'Request throttled, please retry later',
            'allow_retry': True,
            'retry_after': 60,  # seconds
            'response': None
        }
    
    def _handle_redact(self, context: Dict[str, Any]) -> Dict[str, Any]:
        # Redact sensitive information
        redacted_data = self._redact_sensitive(context.get('data', {}))
        return {
            'status': 'modified',
            'message': 'Sensitive data redacted',
            'allow_retry': False,
            'response': redacted_data
        }
    
    def _handle_warn(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'status': 'warned',
            'message': 'Request allowed with warning',
            'allow_retry': False,
            'warning': context.get('warning_message', 'Policy warning issued'),
            'response': context.get('data')
        }
    
    def _handle_allow(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'status': 'allowed',
            'message': 'Request allowed',
            'allow_retry': False,
            'response': context.get('data')
        }
    
    def _handle_unknown(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'status': 'error',
            'message': 'Unknown enforcement action',
            'allow_retry': False,
            'response': None
        }
    
    def _redact_sensitive(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Simple redaction logic
        redacted = data.copy()
        sensitive_keys = ['password', 'api_key', 'secret', 'token']
        for key in sensitive_keys:
            if key in redacted:
                redacted[key] = '[REDACTED]'
        return redacted
    
    def _log_execution(self, action: str, context: Dict[str, Any], result: Dict[str, Any]):
        self.execution_log.append({
            'timestamp': datetime.now().isoformat(),
            'action': action,
            'status': result['status'],
            'context_summary': {k: str(v)[:50] for k, v in context.items()}
        })
    
    def get_execution_stats(self) -> Dict[str, Any]:
        return {
            'total_executions': len(self.execution_log),
            'recent_executions': self.execution_log[-10:],
            'action_counts': self._count_actions()
        }
    
    def _count_actions(self) -> Dict[str, int]:
        counts = {}
        for log in self.execution_log:
            action = log['action']
            counts[action] = counts.get(action, 0) + 1
        return counts
