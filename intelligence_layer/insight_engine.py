"""
Insight Engine - Analytics and learning insights
Integrated from AI-ASSISTANT repository
"""
from typing import Dict, Any, List
from datetime import datetime
from collections import defaultdict

class InsightEngine:
    """Generates insights from user interactions and system behavior"""
    
    def __init__(self):
        self.interaction_log: List[Dict[str, Any]] = []
        self.insights_cache: Dict[str, Any] = {}
    
    def log_interaction(self, user_id: str, query: str, result: Any, metadata: Dict[str, Any] = None):
        """Log user interaction for analysis"""
        self.interaction_log.append({
            "user_id": user_id,
            "query": query,
            "result": result,
            "metadata": metadata or {},
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def generate_user_insights(self, user_id: str) -> Dict[str, Any]:
        """Generate insights for specific user"""
        user_interactions = [i for i in self.interaction_log if i["user_id"] == user_id]
        
        if not user_interactions:
            return {"user_id": user_id, "insights": "No data available"}
        
        return {
            "user_id": user_id,
            "total_interactions": len(user_interactions),
            "first_interaction": user_interactions[0]["timestamp"],
            "last_interaction": user_interactions[-1]["timestamp"],
            "common_queries": self._get_common_patterns(user_interactions)
        }
    
    def generate_system_insights(self) -> Dict[str, Any]:
        """Generate system-wide insights"""
        if not self.interaction_log:
            return {"insights": "No data available"}
        
        user_counts = defaultdict(int)
        for interaction in self.interaction_log:
            user_counts[interaction["user_id"]] += 1
        
        return {
            "total_interactions": len(self.interaction_log),
            "unique_users": len(user_counts),
            "most_active_user": max(user_counts.items(), key=lambda x: x[1])[0] if user_counts else None,
            "average_interactions_per_user": len(self.interaction_log) / len(user_counts) if user_counts else 0
        }
    
    def _get_common_patterns(self, interactions: List[Dict[str, Any]]) -> List[str]:
        """Extract common patterns from interactions"""
        queries = [i["query"] for i in interactions]
        # Simple pattern detection - count word frequency
        words = defaultdict(int)
        for query in queries:
            for word in str(query).lower().split():
                if len(word) > 3:  # Skip short words
                    words[word] += 1
        
        # Return top 5 common words
        return [word for word, _ in sorted(words.items(), key=lambda x: x[1], reverse=True)[:5]]

# Global insight engine instance
insight_engine = InsightEngine()

def insightflow_hook(user_id: str, query: str, result: Any, metadata: Dict[str, Any] = None):
    """Hook for logging insights (backward compatibility)"""
    insight_engine.log_interaction(user_id, query, result, metadata)
