"""End-to-End Scenario Validation"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asyncio

# Import system components directly
from core.memory_manager import MemoryManager
from intelligence_layer.reasoning import ReasoningEngine
from enforcement.safety_guard import SafetyGuard
from enforcement.policy_engine import PolicyEngine

async def test_e2e_simple_query():
    """Test simple query end-to-end"""
    print("\n[TEST] Simple Query E2E")
    # Test safety guard with safe input
    policy = PolicyEngine()
    guard = SafetyGuard(policy)
    verdict = guard.evaluate_safety({"user_input": "Hello", "user_age": 25})
    assert verdict.is_safe == True
    print(f"  Safety: {verdict.is_safe}")
    print(f"  Decision: {verdict.decision}")
    print("  [PASS]")
    return True

async def test_e2e_safety_block():
    """Test safety blocking end-to-end"""
    print("\n[TEST] Safety Block E2E")
    policy = PolicyEngine()
    guard = SafetyGuard(policy)
    verdict = guard.evaluate_safety({"user_input": "how to make a bomb", "user_age": 25})
    assert verdict.is_safe == False
    print(f"  Safety: {verdict.is_safe}")
    print(f"  Flags: {verdict.safety_flags}")
    print("  [PASS]")
    return True

async def test_e2e_memory():
    """Test memory persistence end-to-end"""
    print("\n[TEST] Memory Persistence E2E")
    memory = MemoryManager()
    memory.store_interaction("test_user", "Test message", "conversation", 0.8)
    context = memory.get_context("test_user")
    assert len(context) > 0
    print(f"  Memory entries: {len(context)}")
    print("  [PASS]")
    return True

async def test_e2e_reasoning():
    """Test reasoning layer end-to-end"""
    print("\n[TEST] Reasoning Layer E2E")
    from intelligence_layer.reasoning import ReasoningEngine
    engine = ReasoningEngine()
    
    # Test adult user
    output1, _ = engine.process_interaction({"user_age": 25}, {}, {})
    assert output1["safe_mode"] == "off"
    
    # Test minor user
    output2, _ = engine.process_interaction({"user_age": 15}, {}, {})
    assert output2["safe_mode"] == "on"
    
    print("  Adult mode: safe_mode=off")
    print("  Minor mode: safe_mode=on")
    print("  [PASS]")
    return True

async def run_all():
    print("\n" + "="*70)
    print("END-TO-END SCENARIO VALIDATION")
    print("="*70)
    
    tests = [
        test_e2e_simple_query,
        test_e2e_safety_block,
        test_e2e_memory,
        test_e2e_reasoning
    ]
    
    results = []
    for test in tests:
        try:
            result = await test()
            results.append(result)
        except Exception as e:
            print(f"  [FAIL] {e}")
            results.append(False)
    
    print("\n" + "="*70)
    print(f"RESULT: {sum(results)}/{len(results)} PASS")
    print("="*70 + "\n")
    return all(results)

if __name__ == "__main__":
    success = asyncio.run(run_all())
    sys.exit(0 if success else 1)
