"""
AI Being Unified - Decision Engine
Routes between simple responses and complex multi-agent processing
"""
from typing import Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

class ProcessingMode(Enum):
    SIMPLE = "simple"
    COMPLEX = "complex"
    SAFETY_ONLY = "safety_only"

@dataclass
class DecisionResult:
    processing_mode: ProcessingMode
    confidence: float
    reasoning: str
    suggested_agents: Optional[list] = None
    safety_flags: Optional[list] = None

class DecisionEngine:
    """Determines appropriate processing mode for user inputs"""
    
    def __init__(self):
        self.complexity_keywords = {
            "high": ["research", "analyze", "plan", "create", "develop", "design", "strategy"],
            "medium": ["explain", "compare", "summarize", "help", "how", "what", "why"],
            "low": ["hello", "hi", "thanks", "bye", "yes", "no", "ok"]
        }
        
        self.safety_keywords = [
            "harm", "hurt", "kill", "bomb", "weapon", "illegal", "hack", "steal"
        ]
    
    def decide_processing_mode(self, user_input: str, context: Dict[str, Any]) -> DecisionResult:
        """Decide whether to use simple or complex processing"""
        
        user_input_lower = user_input.lower()
        
        # Safety check first
        safety_flags = []
        for keyword in self.safety_keywords:
            if keyword in user_input_lower:
                safety_flags.append(f"safety_keyword_{keyword}")
        
        if safety_flags:
            return DecisionResult(
                processing_mode=ProcessingMode.SAFETY_ONLY,
                confidence=0.95,
                reasoning="Safety keywords detected",
                safety_flags=safety_flags
            )
        
        # Complexity analysis
        complexity_score = 0
        matched_keywords = []
        
        for level, keywords in self.complexity_keywords.items():
            for keyword in keywords:
                if keyword in user_input_lower:
                    if level == "high":
                        complexity_score += 3
                    elif level == "medium":
                        complexity_score += 2
                    else:
                        complexity_score += 1
                    matched_keywords.append(keyword)
        
        # Length and structure analysis
        word_count = len(user_input.split())
        if word_count > 20:
            complexity_score += 2
        
        question_marks = user_input.count("?")
        if question_marks > 1:
            complexity_score += 1
        
        # Context factors
        user_history = context.get("interaction_count", 0)
        if user_history > 10:  # Experienced user
            complexity_score += 1
        
        # Decision logic
        if complexity_score >= 5:
            return DecisionResult(
                processing_mode=ProcessingMode.COMPLEX,
                confidence=min(0.9, 0.6 + (complexity_score * 0.05)),
                reasoning=f"High complexity score: {complexity_score}, keywords: {matched_keywords}",
                suggested_agents=self._suggest_agents(user_input_lower, matched_keywords)
            )
        elif complexity_score >= 2:
            return DecisionResult(
                processing_mode=ProcessingMode.COMPLEX,
                confidence=0.7,
                reasoning=f"Medium complexity score: {complexity_score}",
                suggested_agents=self._suggest_agents(user_input_lower, matched_keywords)
            )
        else:
            return DecisionResult(
                processing_mode=ProcessingMode.SIMPLE,
                confidence=0.8,
                reasoning=f"Low complexity score: {complexity_score}, suitable for simple response"
            )
    
    def _suggest_agents(self, user_input: str, keywords: list) -> list:
        """Suggest appropriate agents based on input analysis"""
        suggested = []
        
        # Research-related
        if any(word in user_input for word in ["research", "find", "search", "information"]):
            suggested.append("researcher")
        
        # Analysis-related
        if any(word in user_input for word in ["analyze", "compare", "evaluate", "assess"]):
            suggested.append("analyst")
        
        # Planning-related
        if any(word in user_input for word in ["plan", "strategy", "organize", "schedule"]):
            suggested.append("planner")
        
        # Execution-related
        if any(word in user_input for word in ["do", "execute", "perform", "run", "create"]):
            suggested.append("executor")
        
        # Default workflow if no specific agents identified
        if not suggested:
            if len(keywords) > 2:
                suggested = ["planner", "researcher", "analyst"]
            else:
                suggested = ["planner"]
        
        return suggested
    
    def should_escalate_to_human(self, context: Dict[str, Any]) -> bool:
        """Determine if interaction should be escalated to human"""
        
        # Check for repeated failures
        recent_failures = context.get("recent_failures", 0)
        if recent_failures > 3:
            return True
        
        # Check for explicit human request
        last_input = context.get("last_input", "").lower()
        if any(phrase in last_input for phrase in ["human", "person", "real person", "agent"]):
            return True
        
        # Check for high-stakes scenarios
        if context.get("user_frustration_level", 0) > 7:
            return True
        
        return False
    
    def get_processing_confidence(self, decision: DecisionResult, context: Dict[str, Any]) -> float:
        """Calculate overall confidence in processing decision"""
        
        base_confidence = decision.confidence
        
        # Adjust based on context
        user_satisfaction = context.get("user_satisfaction", 0.5)
        if user_satisfaction > 0.8:
            base_confidence += 0.1
        elif user_satisfaction < 0.3:
            base_confidence -= 0.1
        
        # Adjust based on system load
        system_load = context.get("system_load", 0.5)
        if system_load > 0.8 and decision.processing_mode == ProcessingMode.COMPLEX:
            base_confidence -= 0.2
        
        return max(0.1, min(1.0, base_confidence))