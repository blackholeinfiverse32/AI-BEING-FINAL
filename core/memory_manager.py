"""
AI Being Unified - Memory Manager
Handles persistent state, context, and user profiles
"""
import json
import os
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict

@dataclass
class MemoryEntry:
    id: str
    content: str
    timestamp: datetime
    context_type: str
    importance: float
    user_id: str

@dataclass
class UserProfile:
    user_id: str
    preferences: Dict[str, Any]
    interaction_history: List[str]
    trust_level: float
    created_at: datetime
    last_active: datetime

class MemoryManager:
    def __init__(self, storage_path: str = "memory"):
        self.storage_path = storage_path
        self.short_term_memory = {}  # Session-based
        self.long_term_memory = {}   # Persistent
        self.user_profiles = {}      # User data
        self.context_window = 10     # Number of recent interactions to keep in context
        
        self._ensure_storage_exists()
        self._load_persistent_data()
    
    def _ensure_storage_exists(self):
        """Create storage directory if it doesn't exist"""
        os.makedirs(self.storage_path, exist_ok=True)
    
    def _load_persistent_data(self):
        """Load persistent memory and user profiles"""
        # Load long-term memory
        ltm_path = os.path.join(self.storage_path, "long_term_memory.json")
        if os.path.exists(ltm_path):
            with open(ltm_path, 'r') as f:
                data = json.load(f)
                self.long_term_memory = {k: MemoryEntry(**v) for k, v in data.items()}
        
        # Load user profiles
        profiles_path = os.path.join(self.storage_path, "user_profiles.json")
        if os.path.exists(profiles_path):
            with open(profiles_path, 'r') as f:
                data = json.load(f)
                self.user_profiles = {k: UserProfile(**v) for k, v in data.items()}
    
    def _save_persistent_data(self):
        """Save persistent memory and user profiles"""
        # Save long-term memory
        ltm_path = os.path.join(self.storage_path, "long_term_memory.json")
        with open(ltm_path, 'w') as f:
            data = {k: asdict(v) for k, v in self.long_term_memory.items()}
            json.dump(data, f, indent=2, default=str)
        
        # Save user profiles
        profiles_path = os.path.join(self.storage_path, "user_profiles.json")
        with open(profiles_path, 'w') as f:
            data = {k: asdict(v) for k, v in self.user_profiles.items()}
            json.dump(data, f, indent=2, default=str)
    
    def store_interaction(self, user_id: str, content: str, context_type: str = "conversation", importance: float = 0.5):
        """Store an interaction in memory"""
        entry_id = f"{user_id}_{datetime.now().isoformat()}"
        
        entry = MemoryEntry(
            id=entry_id,
            content=content,
            timestamp=datetime.now(),
            context_type=context_type,
            importance=importance,
            user_id=user_id
        )
        
        # Store in short-term memory
        if user_id not in self.short_term_memory:
            self.short_term_memory[user_id] = []
        self.short_term_memory[user_id].append(entry)
        
        # Keep only recent entries in short-term
        self.short_term_memory[user_id] = self.short_term_memory[user_id][-self.context_window:]
        
        # Store important entries in long-term memory
        if importance > 0.7:
            self.long_term_memory[entry_id] = entry
            self._save_persistent_data()
    
    def get_context(self, user_id: str, include_long_term: bool = True) -> List[MemoryEntry]:
        """Retrieve context for a user"""
        context = []
        
        # Add short-term memory
        if user_id in self.short_term_memory:
            context.extend(self.short_term_memory[user_id])
        
        # Add relevant long-term memory
        if include_long_term:
            relevant_ltm = [
                entry for entry in self.long_term_memory.values()
                if entry.user_id == user_id and entry.importance > 0.6
            ]
            # Sort by importance and recency
            relevant_ltm.sort(key=lambda x: (x.importance, x.timestamp), reverse=True)
            context.extend(relevant_ltm[:5])  # Top 5 most relevant
        
        return sorted(context, key=lambda x: x.timestamp)
    
    def get_user_profile(self, user_id: str) -> UserProfile:
        """Get or create user profile"""
        if user_id not in self.user_profiles:
            self.user_profiles[user_id] = UserProfile(
                user_id=user_id,
                preferences={},
                interaction_history=[],
                trust_level=0.5,
                created_at=datetime.now(),
                last_active=datetime.now()
            )
            self._save_persistent_data()
        
        return self.user_profiles[user_id]
    
    def update_user_profile(self, user_id: str, updates: Dict[str, Any]):
        """Update user profile"""
        profile = self.get_user_profile(user_id)
        
        for key, value in updates.items():
            if hasattr(profile, key):
                setattr(profile, key, value)
            else:
                profile.preferences[key] = value
        
        profile.last_active = datetime.now()
        self._save_persistent_data()
    
    def clear_session(self, user_id: str):
        """Clear short-term memory for a user"""
        if user_id in self.short_term_memory:
            del self.short_term_memory[user_id]
    
    def cleanup_old_memories(self, days_old: int = 30):
        """Remove old memories to prevent storage bloat"""
        cutoff_date = datetime.now() - timedelta(days=days_old)
        
        # Clean long-term memory
        to_remove = [
            entry_id for entry_id, entry in self.long_term_memory.items()
            if entry.timestamp < cutoff_date and entry.importance < 0.8
        ]
        
        for entry_id in to_remove:
            del self.long_term_memory[entry_id]
        
        if to_remove:
            self._save_persistent_data()
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Get memory usage statistics"""
        return {
            "short_term_entries": sum(len(entries) for entries in self.short_term_memory.values()),
            "long_term_entries": len(self.long_term_memory),
            "user_profiles": len(self.user_profiles),
            "active_sessions": len(self.short_term_memory)
        }