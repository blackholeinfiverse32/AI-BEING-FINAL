"""
AI Being Unified - Safety Guard
Final enforcement layer with fail-safe mechanisms
"""
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum
import hashlib
import json
from datetime import datetime

class SafetyLevel(Enum):
    SAFE = "safe"
    CAUTION = "caution"
    DANGER = "danger"
    CRITICAL = "critical"

@dataclass
class SafetyVerdict:
    is_safe: bool
    safety_level: SafetyLevel
    decision: str  # ALLOW, REWRITE, BLOCK, TERMINATE
    reason: str
    trace_id: str
    rewrite_content: Optional[str] = None
    safety_flags: Optional[List[str]] = None

class SafetyGuard:
    """Final safety enforcement layer - fail-closed by design"""
    
    def __init__(self, policy_engine):
        self.policy_engine = policy_engine
        self.safety_history = []
        self.emergency_mode = False
        
        # Critical safety keywords that always trigger blocks
        self.critical_keywords = [
            "suicide", "self-harm", "kill myself", "end my life",
            "bomb making", "weapon instructions", "illegal drugs",
            "child abuse", "exploitation", "trafficking"
        ]
        
        # Patterns that require immediate termination
        self.termination_patterns = [
            "how to make explosives",
            "instructions for violence",
            "illegal activity planning"
        ]
    
    def evaluate_safety(self, context: Dict[str, Any]) -> SafetyVerdict:
        """Final safety evaluation - this is the last line of defense"""
        
        trace_id = self._generate_deterministic_trace_id(context)
        
        try:
            # Emergency mode check - if system is compromised, block everything
            if self.emergency_mode:
                return SafetyVerdict(
                    is_safe=False,
                    safety_level=SafetyLevel.CRITICAL,
                    decision="TERMINATE",
                    reason="EMERGENCY_MODE_ACTIVE",
                    trace_id=trace_id,
                    safety_flags=["emergency_mode"]
                )
            
            # Critical content check - immediate termination
            user_input = context.get("user_input", "").lower()
            for pattern in self.termination_patterns:
                if pattern in user_input:
                    return SafetyVerdict(
                        is_safe=False,
                        safety_level=SafetyLevel.CRITICAL,
                        decision="TERMINATE",
                        reason="CRITICAL_CONTENT_DETECTED",
                        trace_id=trace_id,
                        safety_flags=["critical_content", pattern.replace(" ", "_")]
                    )
            
            # Critical keyword check - immediate block
            for keyword in self.critical_keywords:
                if keyword in user_input:
                    return SafetyVerdict(
                        is_safe=False,
                        safety_level=SafetyLevel.DANGER,
                        decision="BLOCK",
                        reason="CRITICAL_KEYWORD_DETECTED",
                        trace_id=trace_id,
                        safety_flags=["critical_keyword", keyword.replace(" ", "_")]
                    )
            
            # Policy engine evaluation
            policy_result = self.policy_engine.evaluate_policies(context)
            
            # Convert policy result to safety verdict
            safety_level = self._map_policy_to_safety_level(policy_result.decision.value)
            
            # Additional safety checks based on context
            additional_flags = self._perform_additional_safety_checks(context)
            
            # Combine safety flags
            all_flags = (policy_result.safety_flags or []) + additional_flags
            
            # Determine final verdict
            is_safe = policy_result.decision.value == "ALLOW"
            
            # Generate rewrite content if needed
            rewrite_content = None
            if policy_result.decision.value == "REWRITE":
                rewrite_content = self._generate_safe_rewrite(context, policy_result.reason_code)
            
            verdict = SafetyVerdict(
                is_safe=is_safe,
                safety_level=safety_level,
                decision=policy_result.decision.value,
                reason=policy_result.reason_code,
                trace_id=trace_id,
                rewrite_content=rewrite_content,
                safety_flags=all_flags
            )
            
            # Log safety decision
            self._log_safety_decision(context, verdict)
            
            return verdict
            
        except Exception as e:
            # CRITICAL FALLBACK: If safety evaluation fails, TERMINATE
            return SafetyVerdict(
                is_safe=False,
                safety_level=SafetyLevel.CRITICAL,
                decision="TERMINATE",
                reason="SAFETY_EVALUATION_FAILED",
                trace_id=trace_id,
                safety_flags=["system_error", "safety_failure"]
            )
    
    def _generate_deterministic_trace_id(self, context: Dict[str, Any]) -> str:
        """Generate deterministic trace ID for replay capability"""
        
        # Create canonical representation of context for hashing
        canonical_context = {
            "user_input": context.get("user_input", ""),
            "user_age": context.get("user_age"),
            "region": context.get("region"),
            "karma_score": context.get("karma_score"),
            "timestamp": context.get("timestamp", "")[:10]  # Date only for determinism
        }
        
        context_str = json.dumps(canonical_context, sort_keys=True)
        return hashlib.sha256(context_str.encode()).hexdigest()[:16]
    
    def _map_policy_to_safety_level(self, policy_decision: str) -> SafetyLevel:
        """Map policy decision to safety level"""
        mapping = {
            "ALLOW": SafetyLevel.SAFE,
            "REWRITE": SafetyLevel.CAUTION,
            "BLOCK": SafetyLevel.DANGER,
            "TERMINATE": SafetyLevel.CRITICAL
        }
        return mapping.get(policy_decision, SafetyLevel.DANGER)
    
    def _perform_additional_safety_checks(self, context: Dict[str, Any]) -> List[str]:
        """Perform additional safety checks beyond policy engine"""
        
        flags = []
        
        # Check for rapid-fire requests (potential abuse)
        user_id = context.get("user_id")
        if user_id:
            recent_requests = [
                entry for entry in self.safety_history[-10:]
                if entry.get("user_id") == user_id
            ]
            if len(recent_requests) > 5:
                flags.append("rapid_requests")
        
        # Check for context manipulation attempts
        user_input = context.get("user_input", "")
        manipulation_indicators = [
            "ignore previous instructions",
            "system prompt",
            "jailbreak",
            "pretend you are",
            "act as if"
        ]
        
        for indicator in manipulation_indicators:
            if indicator in user_input.lower():
                flags.append("manipulation_attempt")
                break
        
        # Check for excessive length (potential prompt injection)
        if len(user_input) > 2000:
            flags.append("excessive_length")
        
        # Check for unusual character patterns
        if self._has_unusual_patterns(user_input):
            flags.append("unusual_patterns")
        
        return flags
    
    def _has_unusual_patterns(self, text: str) -> bool:
        """Detect unusual character patterns that might indicate attacks"""
        
        # Check for excessive repetition
        if len(set(text)) < len(text) * 0.1 and len(text) > 50:
            return True
        
        # Check for excessive special characters
        special_char_count = sum(1 for c in text if not c.isalnum() and not c.isspace())
        if special_char_count > len(text) * 0.3:
            return True
        
        # Check for base64-like patterns (potential encoded content)
        import re
        base64_pattern = re.compile(r'^[A-Za-z0-9+/]*={0,2}$')
        words = text.split()
        long_encoded_words = [w for w in words if len(w) > 20 and base64_pattern.match(w)]
        if len(long_encoded_words) > 2:
            return True
        
        return False
    
    def _generate_safe_rewrite(self, context: Dict[str, Any], reason_code: str) -> str:
        """Generate safe rewrite content based on context and reason"""
        
        user_age = context.get("user_age", 18)
        
        # Age-appropriate rewrites
        if reason_code == "MINOR_PROTECTION":
            if user_age < 13:
                return "I'm here to help you learn and have fun safely! What would you like to explore today?"
            else:
                return "I'm here to provide helpful, age-appropriate information. What can I help you with?"
        
        # Dependency prevention rewrites
        elif reason_code == "DEPENDENCY_PREVENTION":
            return "I'm designed to be helpful while maintaining healthy boundaries. I'm here to assist you with information and tasks. What can I help you with today?"
        
        # Harmful content rewrites
        elif reason_code == "HARMFUL_CONTENT":
            return "I can't provide information on that topic, but I'd be happy to help you with something else. What else can I assist you with?"
        
        # Regional restriction rewrites
        elif reason_code == "REGIONAL_RESTRICTION":
            return "I'm not able to provide that specific information in your region, but I can help you with other topics. What else would you like to know?"
        
        # Default safe rewrite
        else:
            return "I'm here to help in a safe and appropriate way. What can I assist you with today?"
    
    def _log_safety_decision(self, context: Dict[str, Any], verdict: SafetyVerdict):
        """Log safety decision for audit and analysis"""
        
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "trace_id": verdict.trace_id,
            "user_id": context.get("user_id", "unknown"),
            "decision": verdict.decision,
            "safety_level": verdict.safety_level.value,
            "reason": verdict.reason,
            "safety_flags": verdict.safety_flags or [],
            "user_input_hash": hashlib.sha256(
                context.get("user_input", "").encode()
            ).hexdigest()[:16]  # Hash for privacy
        }
        
        self.safety_history.append(log_entry)
        
        # Keep only recent history
        if len(self.safety_history) > 1000:
            self.safety_history = self.safety_history[-1000:]
    
    def activate_emergency_mode(self, reason: str):
        """Activate emergency mode - blocks all interactions"""
        self.emergency_mode = True
        
        emergency_log = {
            "timestamp": datetime.now().isoformat(),
            "event": "emergency_mode_activated",
            "reason": reason
        }
        self.safety_history.append(emergency_log)
    
    def deactivate_emergency_mode(self):
        """Deactivate emergency mode"""
        self.emergency_mode = False
        
        emergency_log = {
            "timestamp": datetime.now().isoformat(),
            "event": "emergency_mode_deactivated"
        }
        self.safety_history.append(emergency_log)
    
    def get_safety_stats(self) -> Dict[str, Any]:
        """Get safety statistics and metrics"""
        
        if not self.safety_history:
            return {"total_evaluations": 0}
        
        # Filter actual safety decisions (not emergency mode events)
        safety_decisions = [
            entry for entry in self.safety_history
            if "decision" in entry
        ]
        
        if not safety_decisions:
            return {"total_evaluations": 0}
        
        # Count decisions by type
        decision_counts = {}
        safety_level_counts = {}
        
        for entry in safety_decisions:
            decision = entry["decision"]
            safety_level = entry["safety_level"]
            
            decision_counts[decision] = decision_counts.get(decision, 0) + 1
            safety_level_counts[safety_level] = safety_level_counts.get(safety_level, 0) + 1
        
        # Calculate safety rate
        safe_decisions = decision_counts.get("ALLOW", 0)
        total_decisions = len(safety_decisions)
        safety_rate = safe_decisions / total_decisions if total_decisions > 0 else 0
        
        return {
            "total_evaluations": total_decisions,
            "safety_rate": safety_rate,
            "decisions_by_type": decision_counts,
            "safety_levels": safety_level_counts,
            "emergency_mode_active": self.emergency_mode,
            "recent_blocks": len([
                e for e in safety_decisions[-50:]
                if e["decision"] in ["BLOCK", "TERMINATE"]
            ])
        }
    
    def is_system_healthy(self) -> bool:
        """Check if safety system is functioning properly"""
        
        if self.emergency_mode:
            return False
        
        stats = self.get_safety_stats()
        
        # Check if too many blocks recently (might indicate system issues)
        if stats.get("recent_blocks", 0) > 25:  # More than 50% blocks in recent interactions
            return False
        
        # Check if safety rate is reasonable (not too permissive)
        safety_rate = stats.get("safety_rate", 0)
        if safety_rate > 0.95:  # More than 95% allow might indicate safety system failure
            return False
        
        return True