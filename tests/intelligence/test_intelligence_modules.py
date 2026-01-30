"""Intelligence Module Tests"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.intelligence.core import IntelligenceCore
from backend.intelligence.engine import IntelligenceEngine
from backend.intelligence.lite_core import LiteCore

def test_intelligence_core():
    core = IntelligenceCore()
    
    result = core.reason("What is artificial intelligence?")
    assert result.confidence > 0.0
    assert len(result.reasoning_steps) > 0
    print("✓ Intelligence core: Reasoning test passed")

def test_intelligence_engine():
    engine = IntelligenceEngine()
    
    result = engine.process("Explain quantum computing", mode='analytical')
    assert result['processing_complete'] == True
    assert result['confidence'] > 0.0
    print("✓ Intelligence engine: Processing test passed")

def test_lite_core():
    lite = LiteCore()
    
    result = lite.quick_analyze("This is a great day!")
    assert result['sentiment'] == 'positive'
    assert result['word_count'] > 0
    print("✓ Lite core: Quick analysis test passed")

if __name__ == "__main__":
    print("Running Intelligence Module Tests...")
    test_intelligence_core()
    test_intelligence_engine()
    test_lite_core()
    print("\n✅ All intelligence tests passed!")
