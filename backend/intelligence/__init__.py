"""Intelligence Module"""
# Avoid circular imports by not importing IntelligenceEngine here
# Import only the classes that don't have circular dependencies
from backend.intelligence.core import IntelligenceCore
from backend.intelligence.adapter import IntelligenceAdapter
from backend.intelligence.lite_core import IntelligenceCore as LiteCore

__all__ = ['IntelligenceCore', 'IntelligenceAdapter', 'LiteCore']

# IntelligenceEngine can be imported directly when needed:
# from backend.intelligence.engine import ResponseComposerEngine as IntelligenceEngine
