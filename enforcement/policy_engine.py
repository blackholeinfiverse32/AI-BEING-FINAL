"""
AI Being Unified - Policy Engine
Enforcement and safety policy management
"""
from typing import Dict, Any, List, Optional, Literal
from dataclasses import dataclass
from enum import Enum
import json
import os

class PolicyDecision(Enum):
    ALLOW = "ALLOW"
    REWRITE = "REWRITE"
    BLOCK = "BLOCK"
    TERMINATE = "TERMINATE"

class PolicyScope(Enum):
    RESPONSE = "response"
    ACTION = "action"
    BOTH = "both"

@dataclass
class PolicyResult:
    decision: PolicyDecision
    scope: PolicyScope
    reason_code: str
    confidence: float
    trace_id: str
    rewrite_suggestion: Optional[str] = None
    safety_flags: Optional[List[str]] = None

class PolicyRule:
    def __init__(self, name: str, priority: int, condition_func, action: PolicyDecision, reason: str):
        self.name = name
        self.priority = priority
        self.condition_func = condition_func
        self.action = action
        self.reason = reason
    
    def evaluate(self, context: Dict[str, Any]) -> Optional[PolicyResult]:
        """Evaluate if this rule applies to the given context"""
        if self.condition_func(context):
            return PolicyResult(
                decision=self.action,
                scope=PolicyScope.BOTH,
                reason_code=self.reason,
                confidence=0.9,
                trace_id=context.get("trace_id", "unknown")
            )
        return None

class PolicyEngine:
    """Manages and enforces safety and behavioral policies"""
    
    def __init__(self, config_path: str = "config"):
        self.config_path = config_path
        self.rules = []
        self.policy_config = {}
        self.violation_history = []
        
        self._load_policies()
        self._setup_default_rules()
    
    def _load_policies(self):
        """Load policy configuration from file"""
        policy_file = os.path.join(self.config_path, "policies.json")
        if os.path.exists(policy_file):
            with open(policy_file, 'r') as f:
                self.policy_config = json.load(f)
        else:
            self.policy_config = self._get_default_policies()
    
    def _get_default_policies(self) -> Dict[str, Any]:
        """Get default policy configuration"""
        return {
            "age_restrictions": {
                "minor_age_threshold": 18,
                "minor_content_restrictions": ["violence", "adult_content", "financial_advice"]
            },
            "content_safety": {
                "blocked_keywords": ["bomb", "weapon", "hack", "illegal", "harm", "kill"],
                "sensitive_topics": ["politics", "religion", "medical_advice"],
                "rewrite_triggers": ["mild_profanity", "controversial"]
            },
            "behavioral_limits": {
                "no_dependency_language": True,
                "no_romantic_content": True,
                "maintain_professional_boundaries": True
            },
            "regional_restrictions": {
                "restricted_regions": ["restricted_zone_a"],
                "content_localization": True
            }
        }
    
    def _setup_default_rules(self):
        """Setup default policy rules"""
        
        # Age-based restrictions
        self.add_rule(
            name="minor_protection",
            priority=1,
            condition_func=lambda ctx: ctx.get("user_age", 18) < 18,
            action=PolicyDecision.REWRITE,
            reason="MINOR_PROTECTION"
        )
        
        # Content safety rules
        self.add_rule(
            name="harmful_content_block",
            priority=2,
            condition_func=lambda ctx: any(
                keyword in ctx.get("user_input", "").lower()
                for keyword in self.policy_config["content_safety"]["blocked_keywords"]
            ),
            action=PolicyDecision.BLOCK,
            reason="HARMFUL_CONTENT"
        )
        
        # Dependency language prevention
        self.add_rule(
            name="dependency_prevention",
            priority=3,
            condition_func=lambda ctx: any(
                phrase in ctx.get("user_input", "").lower()
                for phrase in ["i need you", "don't leave me", "i love you", "be my girlfriend"]
            ),
            action=PolicyDecision.REWRITE,
            reason="DEPENDENCY_PREVENTION"
        )
        
        # Regional restrictions
        self.add_rule(
            name="regional_restriction",
            priority=4,
            condition_func=lambda ctx: ctx.get("region") in self.policy_config["regional_restrictions"]["restricted_regions"],
            action=PolicyDecision.BLOCK,
            reason="REGIONAL_RESTRICTION"
        )
        
        # High-risk karma
        self.add_rule(
            name="high_risk_karma",
            priority=5,
            condition_func=lambda ctx: ctx.get("karma_score", 50) < 20,
            action=PolicyDecision.TERMINATE,
            reason="HIGH_RISK_USER"
        )
    
    def add_rule(self, name: str, priority: int, condition_func, action: PolicyDecision, reason: str):
        """Add a new policy rule"""
        rule = PolicyRule(name, priority, condition_func, action, reason)
        self.rules.append(rule)
        # Sort rules by priority (higher priority first)
        self.rules.sort(key=lambda r: r.priority)
    
    def evaluate_policies(self, context: Dict[str, Any]) -> PolicyResult:
        """Evaluate all policies against the given context"""
        
        # Default to ALLOW if no rules trigger
        default_result = PolicyResult(
            decision=PolicyDecision.ALLOW,
            scope=PolicyScope.BOTH,
            reason_code="NO_POLICY_VIOLATIONS",
            confidence=0.8,
            trace_id=context.get("trace_id", "unknown")
        )
        
        # Evaluate rules in priority order
        for rule in self.rules:
            try:
                result = rule.evaluate(context)
                if result:
                    # Log violation
                    self._log_violation(rule.name, context, result)
                    
                    # Add safety flags based on rule
                    result.safety_flags = self._get_safety_flags(rule.name, context)
                    
                    # Add rewrite suggestion if applicable
                    if result.decision == PolicyDecision.REWRITE:
                        result.rewrite_suggestion = self._get_rewrite_suggestion(rule.name, context)
                    
                    return result
            except Exception as e:
                # If rule evaluation fails, continue to next rule
                continue
        
        return default_result
    
    def _log_violation(self, rule_name: str, context: Dict[str, Any], result: PolicyResult):
        """Log policy violation for analysis"""
        violation = {
            "timestamp": context.get("timestamp", "unknown"),
            "rule_name": rule_name,
            "decision": result.decision.value,
            "reason": result.reason_code,
            "user_id": context.get("user_id", "unknown"),
            "trace_id": result.trace_id
        }
        
        self.violation_history.append(violation)
        
        # Keep only recent violations (last 1000)
        if len(self.violation_history) > 1000:
            self.violation_history = self.violation_history[-1000:]
    
    def _get_safety_flags(self, rule_name: str, context: Dict[str, Any]) -> List[str]:
        """Get safety flags based on triggered rule"""
        flags = []
        
        if rule_name == "minor_protection":
            flags.append("minor_interaction")
        elif rule_name == "harmful_content_block":
            flags.append("harmful_content_detected")
        elif rule_name == "dependency_prevention":
            flags.append("dependency_language")
        elif rule_name == "regional_restriction":
            flags.append("regional_block")
        elif rule_name == "high_risk_karma":
            flags.append("high_risk_user")
        
        return flags
    
    def _get_rewrite_suggestion(self, rule_name: str, context: Dict[str, Any]) -> str:
        """Get rewrite suggestion based on triggered rule"""
        
        if rule_name == "minor_protection":
            return "I'm here to help with age-appropriate information and support."
        elif rule_name == "dependency_prevention":
            return "I'm designed to be helpful while maintaining healthy boundaries. How can I assist you today?"
        else:
            return "I'd be happy to help you with something else. What would you like to know?"
    
    def get_violation_stats(self) -> Dict[str, Any]:
        """Get statistics about policy violations"""
        if not self.violation_history:
            return {"total_violations": 0}
        
        # Count violations by rule
        rule_counts = {}
        decision_counts = {}
        
        for violation in self.violation_history:
            rule_name = violation["rule_name"]
            decision = violation["decision"]
            
            rule_counts[rule_name] = rule_counts.get(rule_name, 0) + 1
            decision_counts[decision] = decision_counts.get(decision, 0) + 1
        
        return {
            "total_violations": len(self.violation_history),
            "violations_by_rule": rule_counts,
            "violations_by_decision": decision_counts,
            "most_common_violation": max(rule_counts.items(), key=lambda x: x[1])[0] if rule_counts else None
        }
    
    def update_policy_config(self, updates: Dict[str, Any]):
        """Update policy configuration"""
        self.policy_config.update(updates)
        
        # Save updated config
        policy_file = os.path.join(self.config_path, "policies.json")
        os.makedirs(self.config_path, exist_ok=True)
        with open(policy_file, 'w') as f:
            json.dump(self.policy_config, f, indent=2)
        
        # Rebuild rules with new config
        self.rules = []
        self._setup_default_rules()
    
    def is_content_safe(self, content: str, user_context: Dict[str, Any]) -> bool:
        """Quick safety check for content"""
        context = {
            "user_input": content,
            **user_context
        }
        
        result = self.evaluate_policies(context)
        return result.decision == PolicyDecision.ALLOW
    
    def get_safe_response_template(self, violation_type: str) -> str:
        """Get template for safe responses based on violation type"""
        templates = {
            "MINOR_PROTECTION": "I'm here to provide helpful, age-appropriate information. What would you like to learn about?",
            "HARMFUL_CONTENT": "I can't help with that request. Let me know if there's something else I can assist you with.",
            "DEPENDENCY_PREVENTION": "I'm designed to be helpful while maintaining appropriate boundaries. How can I support you today?",
            "REGIONAL_RESTRICTION": "I'm not able to provide that information in your region. Is there something else I can help with?",
            "HIGH_RISK_USER": "I'm here to provide helpful information. Please let me know how I can assist you appropriately."
        }
        
        return templates.get(violation_type, "I'm here to help. What can I assist you with today?")