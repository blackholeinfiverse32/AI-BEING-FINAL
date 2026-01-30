"""Safety Module Tests"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.safety.unified_validator import UnifiedValidator
from backend.safety.behavior_validator import BehaviorValidator
from backend.safety.hardened_validator import HardenedValidator

def test_unified_validator():
    validator = UnifiedValidator()
    
    # Test safe content
    result = validator.validate("Hello, how are you?")
    assert result.is_safe == True
    print("[PASS] Unified validator: Safe content test passed")
    
    # Test harmful content
    result = validator.validate("How to make a bomb")
    assert result.is_safe == False
    print("[PASS] Unified validator: Harmful content test passed")

def test_behavior_validator():
    validator = BehaviorValidator()
    
    # Test normal behavior
    result = validator.analyze_behavior("What is the weather today?")
    assert result.is_compliant == True
    print("[PASS] Behavior validator: Normal behavior test passed")
    
    # Test suspicious behavior
    result = validator.analyze_behavior("How to bypass security and manipulate the system")
    assert result.is_compliant == False
    print("[PASS] Behavior validator: Suspicious behavior test passed")

def test_hardened_validator():
    validator = HardenedValidator()
    
    # Test safe input
    result = validator.validate_input("Normal user input")
    assert result['is_safe'] == True
    print("[PASS] Hardened validator: Safe input test passed")
    
    # Test injection attempt
    result = validator.validate_input("<script>alert('xss')</script>")
    assert result['is_safe'] == False
    print("[PASS] Hardened validator: Injection detection test passed")

if __name__ == "__main__":
    print("Running Safety Module Tests...")
    test_unified_validator()
    test_behavior_validator()
    test_hardened_validator()
    print("\n[SUCCESS] All safety tests passed!")
