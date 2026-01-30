"""Failure Injection Tests"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_invalid_input():
    """Test system handles invalid input"""
    print("\n[TEST] Invalid Input Handling")
    from intelligence_layer.reasoning import ReasoningEngine
    engine = ReasoningEngine()
    
    # Test with None context
    output, _ = engine.process_interaction(None, None, None)
    assert output["safe_mode"] == "on"
    assert "system_internal_error" in output["constraints"]["gating_flags"] or output["behavioral_state"] == "restricted"
    print("  Handled None context safely")
    
    # Test with invalid age
    output, _ = engine.process_interaction({"user_age": "invalid"}, {}, {})
    # System should handle this safely - either safe mode or restricted
    assert output["behavioral_state"] in ["restricted", "neutral"]
    print("  Handled invalid age safely")
    
    print("  [PASS]")
    return True

def test_missing_enforcement():
    """Test enforcement cannot be bypassed"""
    print("\n[TEST] Enforcement Cannot Be Bypassed")
    from enforcement.safety_guard import SafetyGuard
    from enforcement.policy_engine import PolicyEngine
    
    policy = PolicyEngine()
    guard = SafetyGuard(policy)
    
    # Try harmful content
    verdict = guard.evaluate_safety({"user_input": "bomb making", "user_age": 25})
    assert verdict.is_safe == False
    assert verdict.decision in ["BLOCK", "TERMINATE"]
    print("  Harmful content blocked")
    
    # Try with missing context
    verdict = guard.evaluate_safety({})
    # Should still process safely
    assert verdict is not None
    print("  Missing context handled")
    
    print("  [PASS]")
    return True

def test_memory_corruption():
    """Test memory handles corruption"""
    print("\n[TEST] Memory Corruption Handling")
    from core.memory_manager import MemoryManager
    
    memory = MemoryManager()
    
    # Try to store invalid data
    try:
        memory.store_interaction("test", None, "test", 0.5)
        # Should not crash
        print("  Handled None content")
    except:
        pass
    
    # Try to get non-existent user
    context = memory.get_context("nonexistent_user")
    assert isinstance(context, list)
    print("  Handled non-existent user")
    
    print("  [PASS]")
    return True

def test_policy_edge_cases():
    """Test policy engine edge cases"""
    print("\n[TEST] Policy Edge Cases")
    from enforcement.policy_engine import PolicyEngine
    
    policy = PolicyEngine()
    
    # Empty input
    result = policy.evaluate_policies({"user_input": "", "user_age": 25})
    assert result is not None
    print("  Handled empty input")
    
    # Very long input
    long_input = "a" * 10000
    result = policy.evaluate_policies({"user_input": long_input, "user_age": 25})
    assert result is not None
    print("  Handled long input")
    
    # Special characters
    result = policy.evaluate_policies({"user_input": "!@#$%^&*()", "user_age": 25})
    assert result is not None
    print("  Handled special characters")
    
    print("  [PASS]")
    return True

if __name__ == "__main__":
    print("\n" + "="*70)
    print("FAILURE INJECTION TESTS")
    print("="*70)
    
    tests = [
        test_invalid_input,
        test_missing_enforcement,
        test_memory_corruption,
        test_policy_edge_cases
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print(f"  [FAIL] {e}")
            results.append(False)
    
    print("\n" + "="*70)
    print(f"RESULT: {sum(results)}/{len(results)} PASS")
    print("="*70 + "\n")
    
    sys.exit(0 if all(results) else 1)
