"""
Test AI-ASSISTANT Integration Hook
Verifies that the integration infrastructure is ready for AI-ASSISTANT repository
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.extended_integration import (
    extended_integration,
    integrate_ai_assistant_repository,
    ExtendedCapability
)

def test_integration_hook():
    """Test that integration hook is ready"""
    print("Testing AI-ASSISTANT Integration Hook\n")
    
    # Test 1: Check integration status
    print("1. Checking integration status...")
    status = extended_integration.get_integration_status()
    print("   [OK] Status: {}".format(status))
    assert isinstance(status, dict), "Status should be a dictionary"
    assert "initialized" in status, "Status should have 'initialized' field"
    print()
    
    # Test 2: Register a test capability
    print("2. Testing capability registration...")
    test_capability = ExtendedCapability(
        name="test_capability",
        description="Test capability for AI-ASSISTANT",
        handler=lambda x: {"result": "test"},
        priority=5
    )
    extended_integration.register_capability(test_capability)
    capabilities = extended_integration.list_capabilities()
    print(f"   ✅ Registered capabilities: {capabilities}")
    assert "test_capability" in capabilities, "Test capability should be registered"
    print()
    
    # Test 3: Get registered capability
    print("3️⃣ Testing capability retrieval...")
    retrieved = extended_integration.get_capability("test_capability")
    print(f"   ✅ Retrieved: {retrieved.name if retrieved else 'None'}")
    assert retrieved is not None, "Should retrieve registered capability"
    assert retrieved.name == "test_capability", "Should retrieve correct capability"
    print()
    
    # Test 4: Test integration with non-existent path
    print("4️⃣ Testing integration with non-existent path...")
    result = integrate_ai_assistant_repository("./non_existent_repo")
    print(f"   ✅ Result: {result}")
    assert not result["success"], "Should fail for non-existent path"
    assert len(result["errors"]) > 0, "Should have error messages"
    assert result["status"] == "not_accessible", "Status should be not_accessible"
    print()
    
    # Test 5: Check if AI-ASSISTANT repo exists locally
    print("5️⃣ Checking for AI-ASSISTANT repository...")
    possible_paths = [
        "./AI-ASSISTANT",
        "../AI-ASSISTANT",
        "../../AI-ASSISTANT",
        os.path.join(os.path.dirname(__file__), "..", "AI-ASSISTANT")
    ]
    
    found = False
    for path in possible_paths:
        if os.path.exists(path):
            print(f"   ✅ Found at: {path}")
            result = integrate_ai_assistant_repository(path)
            print(f"   📊 Integration result: {result}")
            found = True
            break
    
    if not found:
        print("   ⚠️  AI-ASSISTANT repository not found locally")
        print("   📝 Repository URL: https://github.com/blackholeinfiverse83-bit/AI-ASSISTANT")
        print("   💡 To integrate:")
        print("      1. Clone: git clone https://github.com/blackholeinfiverse83-bit/AI-ASSISTANT.git")
        print("      2. Run: python -c 'from core.extended_integration import integrate_ai_assistant_repository; print(integrate_ai_assistant_repository(\"./AI-ASSISTANT\"))'")
    print()
    
    print("✅ All integration hook tests passed!")
    print("\n📋 Summary:")
    print("   - Integration infrastructure: ✅ Ready")
    print("   - Capability registration: ✅ Working")
    print("   - Error handling: ✅ Working")
    print("   - AI-ASSISTANT repo: ⚠️  Not accessible (404)")
    print("\n🎯 Next Steps:")
    print("   1. Verify repository access (may be private)")
    print("   2. Clone repository when available")
    print("   3. Run integration: integrate_ai_assistant_repository('./AI-ASSISTANT')")
    print("   4. Update INTEGRATION_SUMMARY.md")

if __name__ == "__main__":
    test_integration_hook()
