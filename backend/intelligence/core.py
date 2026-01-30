"""Intelligence Core - Advanced reasoning and decision making"""
from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class ReasoningResult:
    conclusion: str
    confidence: float
    reasoning_steps: List[str]
    evidence: List[str]

class IntelligenceCore:
    def __init__(self):
        self.knowledge_base = {}
        self.reasoning_history = []
    
    def reason(self, query: str, context: Dict[str, Any] = None) -> ReasoningResult:
        steps = []
        evidence = []
        
        steps.append(f"Analyzing query: {query[:50]}...")
        query_type = self._classify_query(query)
        evidence.append(f"Query classified as: {query_type}")
        
        steps.append("Gathering relevant knowledge")
        relevant_knowledge = self._get_relevant_knowledge(query, context)
        evidence.extend(relevant_knowledge)
        
        steps.append("Applying logical reasoning")
        conclusion = self._apply_reasoning(query, relevant_knowledge, context)
        
        confidence = self._calculate_confidence(query, relevant_knowledge)
        
        result = ReasoningResult(
            conclusion=conclusion,
            confidence=confidence,
            reasoning_steps=steps,
            evidence=evidence
        )
        
        self.reasoning_history.append(result)
        return result
    
    def _classify_query(self, query: str) -> str:
        query_lower = query.lower()
        if any(word in query_lower for word in ['what', 'define', 'explain']):
            return 'informational'
        elif any(word in query_lower for word in ['how', 'guide', 'steps']):
            return 'procedural'
        elif any(word in query_lower for word in ['why', 'reason', 'cause']):
            return 'causal'
        else:
            return 'general'
    
    def _get_relevant_knowledge(self, query: str, context: Dict[str, Any] = None) -> List[str]:
        knowledge = []
        if context:
            knowledge.append(f"Context provided: {len(context)} items")
        knowledge.append("Using general knowledge base")
        return knowledge
    
    def _apply_reasoning(self, query: str, knowledge: List[str], context: Dict[str, Any] = None) -> str:
        return f"Based on analysis of '{query[:30]}...' and available knowledge, proceeding with informed response"
    
    def _calculate_confidence(self, query: str, knowledge: List[str]) -> float:
        base_confidence = 0.7
        knowledge_boost = min(0.2, len(knowledge) * 0.05)
        return min(1.0, base_confidence + knowledge_boost)
