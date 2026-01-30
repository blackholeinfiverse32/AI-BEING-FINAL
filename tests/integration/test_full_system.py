"""Integration Tests for Complete System"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.orchestration.assistant_orchestrator import AssistantOrchestrator
from backend.safety.enforcement_adapter import EnforcementAdapter
from backend.intelligence.engine import IntelligenceEngine

def test_full_workflow():
    orchestrator = AssistantOrchestrator()
    safety = EnforcementAdapter()
    intelligence = IntelligenceEngine()
    
    orchestrator.initialize_components({
        'safety': safety,
        'intelligence': intelligence
    })
    
    result = orchestrator.orchestrate("What is machine learning?")
    assert result['success'] == True
    assert len(result['workflow']) > 0
    print("[PASS] Full workflow integration test passed")

def test_safety_intelligence_integration():
    safety = EnforcementAdapter()
    intelligence = IntelligenceEngine()
    
    user_input = "Explain neural networks"
    
    safety_result = safety.comprehensive_check(user_input)
    assert safety_result['is_safe'] == True
    
    intel_result = intelligence.process(user_input)
    assert intel_result['processing_complete'] == True
    
    print("[PASS] Safety-Intelligence integration test passed")

if __name__ == "__main__":
    print("Running Integration Tests...")
    test_full_workflow()
    test_safety_intelligence_integration()
    print("\n[SUCCESS] All integration tests passed!")
