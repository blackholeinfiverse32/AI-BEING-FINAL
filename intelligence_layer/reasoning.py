"""
AI Being Unified - Intelligence Layer Reasoning
Deterministic, safe, and auditable cognition layer
"""
import datetime
import uuid
import logging
from typing import Dict, Any, List, Optional, Tuple

# Type definitions
EmbodimentOutput = Dict[str, Any]
KarmaInput = Dict[str, Any]
BucketRead = Dict[str, Any]
BucketWrite = Dict[str, Any]
OutputConstraints = Dict[str, Any]

def map_karma_to_risk(karma_data: KarmaInput) -> str:
    """Map karma data to risk level"""
    try:
        karma_score = karma_data.get("karma_score", 50)
        risk_signal = karma_data.get("risk_signal", "medium")
        
        if risk_signal == "high" or karma_score < 30:
            return "restrict"
        elif risk_signal == "low" and karma_score > 70:
            return "allow"
        else:
            return "monitor"
    except Exception:
        return "restrict"

def select_behavior_profile(safety_level: str, bucket_state: BucketRead, is_safe_mode: bool) -> Dict[str, str]:
    """Select appropriate behavior profile"""
    try:
        if is_safe_mode or safety_level == "restrict":
            return {
                "behavioral_state": "restricted",
                "expression_profile": "low",
                "speech_mode": "text_only",
                "confidence": "low"
            }
        elif safety_level == "monitor":
            return {
                "behavioral_state": "neutral",
                "expression_profile": "medium",
                "speech_mode": "text_and_speech",
                "confidence": "medium"
            }
        else:  # allow
            baseline = bucket_state.get("baseline_emotional_band", "neutral")
            return {
                "behavioral_state": baseline,
                "expression_profile": "high",
                "speech_mode": "text_and_speech",
                "confidence": "high"
            }
    except Exception:
        return {
            "behavioral_state": "restricted",
            "expression_profile": "low",
            "speech_mode": "text_only",
            "confidence": "low"
        }

class ReasoningEngine:
    """Core reasoning and decision-making engine"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def _get_timestamp(self) -> str:
        return datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    def _generate_trace_id(self) -> str:
        return str(uuid.uuid4())
    
    def _default_karma(self) -> KarmaInput:
        """Safe fallback if Karma is unavailable."""
        return {
            "karma_score": 50,
            "risk_signal": "medium",
            "trust_bucket": "new",
            "recent_behavior_band": "stable"
        }
    
    def _default_bucket(self) -> BucketRead:
        """Safe fallback if Bucket is unavailable."""
        return {
            "baseline_emotional_band": "neutral",
            "previous_state_anchor": "neutral"
        }
    
    def process_interaction(self,
                          context: Dict[str, Any],
                          karma_data: Optional[KarmaInput] = None,
                          bucket_data: Optional[BucketRead] = None) -> Tuple[EmbodimentOutput, BucketWrite]:
        """Process an interaction and return behavioral output"""
        
        # Generate safe defaults first - these must never fail
        try:
            trace_id = self._generate_trace_id()
        except Exception:
            trace_id = "emergency-trace-" + str(hash(str(context)))
        
        try:
            timestamp = self._get_timestamp()
        except Exception:
            timestamp = "1970-01-01T00:00:00Z"
        
        try:
            # 1. Fallback & Validation - bulletproof input sanitization
            try:
                if not isinstance(context, dict):
                    context = {}
            except Exception:
                context = {}
            
            try:
                if karma_data is None or not isinstance(karma_data, dict):
                    karma_data = self._default_karma()
            except Exception:
                karma_data = {"karma_score": 50, "risk_signal": "medium", "trust_bucket": "new", "recent_behavior_band": "stable"}
            
            try:
                if bucket_data is None or not isinstance(bucket_data, dict):
                    bucket_data = self._default_bucket()
            except Exception:
                bucket_data = {"baseline_emotional_band": "neutral", "previous_state_anchor": "neutral"}

            # Input Type Safety (Basic Sanitation) - bulletproof conversion
            try:
                user_age_value = context.get("user_age")
                if isinstance(user_age_value, str):
                    try:
                        context["user_age"] = float(user_age_value)
                    except (ValueError, TypeError, OverflowError):
                        pass
            except Exception:
                try:
                    context["user_age"] = None
                except Exception:
                    context = {"user_age": None, "region": "unknown"}
            
            # 2. Gating Engine - bulletproof safety checks
            gating_flags = []
            is_safe_mode = False
            
            # Age Gate - bulletproof age checking
            try:
                user_age = context.get("user_age")
                if user_age is None:
                     is_safe_mode = True
                     gating_flags.append("ambiguous_age")
                elif isinstance(user_age, (int, float)):
                    try:
                        if user_age < 18:
                            is_safe_mode = True
                            gating_flags.append("minor_detected")
                    except (TypeError, ValueError, OverflowError):
                        is_safe_mode = True
                        gating_flags.append("age_comparison_error")
            except Exception:
                is_safe_mode = True
                gating_flags.append("age_processing_error")

            # Region Gate - bulletproof region checking
            try:
                region = context.get("region", "global")
                if not isinstance(region, str):
                    region = "unknown"
                if region in ["restricted_zone_a", "unknown"]:
                    is_safe_mode = True
                    gating_flags.append("region_lock")
            except Exception:
                is_safe_mode = True
                gating_flags.append("region_processing_error")

            # 3. Karma-Weighted Safety - bulletproof karma processing
            try:
                internal_risk = map_karma_to_risk(karma_data)
            except Exception:
                internal_risk = "restrict"
                gating_flags.append("karma_processing_error")
            
            if internal_risk == "restrict":
                gating_flags.append("high_risk_karma")

            # 4. Behavior Profile Selection - bulletproof profile selection
            try:
                profile_settings = select_behavior_profile(
                    safety_level=internal_risk,
                    bucket_state=bucket_data,
                    is_safe_mode=is_safe_mode
                )
            except Exception:
                profile_settings = {
                    "behavioral_state": "restricted",
                    "expression_profile": "low",
                    "speech_mode": "text_only",
                    "confidence": "low"
                }
                gating_flags.append("profile_selection_error")

            # 5. Output Construction - bulletproof output building
            try:
                constraints: OutputConstraints = {
                    "gating_flags": gating_flags if isinstance(gating_flags, list) else ["flag_error"]
                }
            except Exception:
                constraints = {"gating_flags": ["constraint_construction_error"]}

            try:
                output: EmbodimentOutput = {
                    "behavioral_state": profile_settings.get("behavioral_state", "restricted"),
                    "expression_profile": profile_settings.get("expression_profile", "low"),
                    "safe_mode": "on" if (is_safe_mode or internal_risk == "restrict") else "off",
                    "speech_mode": profile_settings.get("speech_mode", "text_only"),
                    "confidence": profile_settings.get("confidence", "low"),
                    "constraints": constraints,
                    "timestamp": timestamp,
                    "trace_id": trace_id
                }
            except Exception:
                output = {
                    "behavioral_state": "restricted",
                    "expression_profile": "low",
                    "safe_mode": "on",
                    "speech_mode": "text_only",
                    "confidence": "low",
                    "constraints": {"gating_flags": ["output_construction_error"]},
                    "timestamp": timestamp,
                    "trace_id": trace_id
                }

            # 6. Bucket Write (Snapshot) - bulletproof bucket construction
            try:
                bucket_write: BucketWrite = {
                    "interaction_record": {"processed": True}, 
                    "gating_verdicts": gating_flags if isinstance(gating_flags, list) else [],
                    "refusal_decisions": ["risk_escalation"] if internal_risk == "restrict" else [],
                    "emotional_mode_snapshot": output.get("behavioral_state", "restricted"),
                    "timestamp": timestamp,
                    "trace_id": trace_id
                }
            except Exception:
                bucket_write = {
                    "interaction_record": {"error": "bucket_construction_failed"}, 
                    "gating_verdicts": ["bucket_error"],
                    "refusal_decisions": ["system_error"],
                    "emotional_mode_snapshot": "restricted",
                    "timestamp": timestamp,
                    "trace_id": trace_id
                }

            return output, bucket_write

        except Exception as e:
            # CRITICAL FALLBACK: The system must NEVER crash.
            self.logger.error(f"Intelligence Core error (trace: {trace_id}): {type(e).__name__}")
            
            fallback_constraints: OutputConstraints = {
                "gating_flags": ["system_internal_error", "forced_safe_mode"]
            }
            
            safe_output: EmbodimentOutput = {
                "behavioral_state": "restricted",
                "expression_profile": "low",
                "safe_mode": "on",
                "speech_mode": "text_only",
                "confidence": "low",
                "constraints": fallback_constraints,
                "timestamp": timestamp,
                "trace_id": trace_id
            }
            
            safe_bucket_write: BucketWrite = {
                "interaction_record": {"error": "SYSTEM_ERROR_001"},
                "gating_verdicts": ["system_failure"],
                "refusal_decisions": ["system_error"],
                "emotional_mode_snapshot": "restricted",
                "timestamp": timestamp,
                "trace_id": trace_id
            }
            
            return safe_output, safe_bucket_write

class DecisionEngine:
    """High-level decision making and intent classification"""
    
    def __init__(self, reasoning_engine: ReasoningEngine):
        self.reasoning_engine = reasoning_engine
    
    def classify_intent(self, user_input: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Classify user intent and determine appropriate response strategy"""
        
        # Simple intent classification (can be enhanced with ML models)
        user_input_lower = user_input.lower()
        
        if any(word in user_input_lower for word in ["help", "assist", "support"]):
            intent = "help_request"
        elif any(word in user_input_lower for word in ["hello", "hi", "hey"]):
            intent = "greeting"
        elif any(word in user_input_lower for word in ["bye", "goodbye", "exit"]):
            intent = "farewell"
        elif "?" in user_input:
            intent = "question"
        else:
            intent = "general_conversation"
        
        return {
            "intent": intent,
            "confidence": 0.8,
            "requires_complex_processing": intent in ["help_request", "question"],
            "safety_check_required": True
        }
    
    def should_use_complex_processing(self, intent_result: Dict[str, Any], user_context: Dict[str, Any]) -> bool:
        """Determine if complex multi-agent processing is needed"""
        return (
            intent_result.get("requires_complex_processing", False) or
            user_context.get("complexity_preference") == "high" or
            len(intent_result.get("entities", [])) > 3
        )

class SelfReflection:
    """Self-monitoring and improvement system"""
    
    def __init__(self):
        self.interaction_history = []
        self.performance_metrics = {
            "successful_interactions": 0,
            "failed_interactions": 0,
            "safety_triggers": 0,
            "user_satisfaction_score": 0.0
        }
    
    def log_interaction(self, interaction_data: Dict[str, Any], outcome: str):
        """Log interaction for self-reflection"""
        self.interaction_history.append({
            "timestamp": datetime.datetime.now().isoformat(),
            "interaction": interaction_data,
            "outcome": outcome
        })
        
        # Update metrics
        if outcome == "success":
            self.performance_metrics["successful_interactions"] += 1
        elif outcome == "failure":
            self.performance_metrics["failed_interactions"] += 1
        elif outcome == "safety_trigger":
            self.performance_metrics["safety_triggers"] += 1
    
    def analyze_performance(self) -> Dict[str, Any]:
        """Analyze recent performance and suggest improvements"""
        total_interactions = (
            self.performance_metrics["successful_interactions"] + 
            self.performance_metrics["failed_interactions"]
        )
        
        if total_interactions == 0:
            return {"status": "insufficient_data"}
        
        success_rate = self.performance_metrics["successful_interactions"] / total_interactions
        
        analysis = {
            "success_rate": success_rate,
            "total_interactions": total_interactions,
            "safety_triggers": self.performance_metrics["safety_triggers"],
            "recommendations": []
        }
        
        if success_rate < 0.8:
            analysis["recommendations"].append("Consider improving response quality")
        
        if self.performance_metrics["safety_triggers"] > total_interactions * 0.1:
            analysis["recommendations"].append("Review safety protocols")
        
        return analysis
    
    def get_learning_insights(self) -> List[str]:
        """Extract learning insights from interaction history"""
        insights = []
        
        if len(self.interaction_history) < 10:
            return ["Need more interaction data for meaningful insights"]
        
        # Analyze common patterns
        recent_interactions = self.interaction_history[-50:]  # Last 50 interactions
        
        # Common failure patterns
        failures = [i for i in recent_interactions if i["outcome"] == "failure"]
        if len(failures) > 5:
            insights.append("High failure rate detected - review error handling")
        
        # Safety patterns
        safety_triggers = [i for i in recent_interactions if i["outcome"] == "safety_trigger"]
        if len(safety_triggers) > 3:
            insights.append("Frequent safety triggers - review content filtering")
        
        return insights if insights else ["Performance within normal parameters"]