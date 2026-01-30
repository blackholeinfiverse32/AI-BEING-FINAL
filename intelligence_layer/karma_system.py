"""
Karma System - User behavior tracking and scoring
Integrated from AI-ASSISTANT repository
"""
from typing import Dict, Any
from datetime import datetime

class KarmaSystem:
    """Tracks user behavior and assigns karma points"""
    
    def __init__(self):
        self.karma_store: Dict[str, Dict[str, Any]] = {}
    
    def track_action(self, user_id: str, action: str, points: int = 10) -> Dict[str, Any]:
        """Track user action and update karma"""
        if user_id not in self.karma_store:
            self.karma_store[user_id] = {
                "total_karma": 0,
                "actions": [],
                "created_at": datetime.utcnow().isoformat()
            }
        
        self.karma_store[user_id]["total_karma"] += points
        self.karma_store[user_id]["actions"].append({
            "action": action,
            "points": points,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        return {
            "karma_points": points,
            "total_karma": self.karma_store[user_id]["total_karma"],
            "user_id": user_id,
            "action": action
        }
    
    def get_karma(self, user_id: str) -> Dict[str, Any]:
        """Get user karma information"""
        if user_id not in self.karma_store:
            return {"user_id": user_id, "total_karma": 0, "actions": []}
        return self.karma_store[user_id]
    
    def get_karma_level(self, user_id: str) -> str:
        """Get user karma level based on points"""
        karma = self.get_karma(user_id)
        total = karma.get("total_karma", 0)
        
        if total < 50:
            return "novice"
        elif total < 200:
            return "intermediate"
        elif total < 500:
            return "advanced"
        else:
            return "expert"

# Global karma system instance
karma_system = KarmaSystem()

def karma_hook(user_id: str, action: str, points: int = 10) -> Dict[str, Any]:
    """Hook for tracking karma (backward compatibility)"""
    return karma_system.track_action(user_id, action, points)
