"""Lite Intelligence Core - Lightweight version for simple operations"""
from typing import Dict, Any

class LiteCore:
    def __init__(self):
        self.cache = {}
    
    def quick_analyze(self, text: str) -> Dict[str, Any]:
        if text in self.cache:
            return self.cache[text]
        
        word_count = len(text.split())
        char_count = len(text)
        
        sentiment = self._detect_sentiment(text)
        intent = self._detect_intent(text)
        
        result = {
            'word_count': word_count,
            'char_count': char_count,
            'sentiment': sentiment,
            'intent': intent,
            'complexity': 'simple' if word_count < 50 else 'moderate' if word_count < 200 else 'complex'
        }
        
        self.cache[text] = result
        return result
    
    def _detect_sentiment(self, text: str) -> str:
        positive_words = ['good', 'great', 'excellent', 'happy', 'love']
        negative_words = ['bad', 'terrible', 'hate', 'sad', 'angry']
        
        text_lower = text.lower()
        pos_count = sum(1 for word in positive_words if word in text_lower)
        neg_count = sum(1 for word in negative_words if word in text_lower)
        
        if pos_count > neg_count:
            return 'positive'
        elif neg_count > pos_count:
            return 'negative'
        else:
            return 'neutral'
    
    def _detect_intent(self, text: str) -> str:
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['?', 'what', 'how', 'why', 'when', 'where']):
            return 'question'
        elif any(word in text_lower for word in ['please', 'can you', 'could you', 'help']):
            return 'request'
        elif any(word in text_lower for word in ['do', 'create', 'make', 'build']):
            return 'command'
        else:
            return 'statement'
