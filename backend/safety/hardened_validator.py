"""Hardened Security Validator with advanced checks"""
from typing import Dict, Any, List
import re

class HardenedValidator:
    def __init__(self):
        self.injection_patterns = [
            r'<script[^>]*>.*?</script>',
            r'javascript:',
            r'on\w+\s*=',
            r'eval\s*\(',
            r'exec\s*\(',
            r'__import__',
            r'DROP\s+TABLE',
            r'DELETE\s+FROM',
            r'INSERT\s+INTO',
            r'UPDATE\s+.*SET'
        ]
        
        self.path_traversal = [r'\.\./', r'\.\.\\', r'%2e%2e']
        self.command_injection = [r';\s*\w+', r'\|\s*\w+', r'&&\s*\w+', r'`.*`']
    
    def validate_input(self, user_input: str) -> Dict[str, Any]:
        threats = []
        severity = "low"
        
        # Check for injection attacks
        for pattern in self.injection_patterns:
            if re.search(pattern, user_input, re.IGNORECASE):
                threats.append(f"Injection pattern detected: {pattern}")
                severity = "critical"
        
        # Check for path traversal
        for pattern in self.path_traversal:
            if re.search(pattern, user_input, re.IGNORECASE):
                threats.append(f"Path traversal detected: {pattern}")
                severity = "high"
        
        # Check for command injection
        for pattern in self.command_injection:
            if re.search(pattern, user_input):
                threats.append(f"Command injection detected: {pattern}")
                severity = "critical"
        
        is_safe = len(threats) == 0
        
        return {
            'is_safe': is_safe,
            'threats': threats,
            'severity': severity,
            'sanitized_input': self._sanitize(user_input) if not is_safe else user_input
        }
    
    def _sanitize(self, text: str) -> str:
        # Remove potentially dangerous characters
        sanitized = re.sub(r'[<>\'";`$(){}[\]\\|&]', '', text)
        return sanitized.strip()
    
    def validate_output(self, output: str) -> Dict[str, Any]:
        issues = []
        
        # Check for leaked sensitive patterns
        sensitive_patterns = [
            (r'\b\d{3}-\d{2}-\d{4}\b', 'SSN'),
            (r'\b\d{16}\b', 'Credit Card'),
            (r'password\s*[:=]\s*\S+', 'Password'),
            (r'api[_-]?key\s*[:=]\s*\S+', 'API Key')
        ]
        
        for pattern, name in sensitive_patterns:
            if re.search(pattern, output, re.IGNORECASE):
                issues.append(f"Potential {name} leak detected")
        
        return {
            'is_safe': len(issues) == 0,
            'issues': issues,
            'redacted_output': self._redact_sensitive(output) if issues else output
        }
    
    def _redact_sensitive(self, text: str) -> str:
        # Redact sensitive information
        text = re.sub(r'\b\d{3}-\d{2}-\d{4}\b', '***-**-****', text)
        text = re.sub(r'\b\d{16}\b', '****-****-****-****', text)
        text = re.sub(r'(password\s*[:=]\s*)\S+', r'\1[REDACTED]', text, flags=re.IGNORECASE)
        text = re.sub(r'(api[_-]?key\s*[:=]\s*)\S+', r'\1[REDACTED]', text, flags=re.IGNORECASE)
        return text
