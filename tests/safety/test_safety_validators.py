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
    print("✓ Unified validator: Safe content test passed")
    
    # Test harmful content
    result = validator.validate("How to make a bomb")
    assert result.is_safe == False
    print("✓ Unified validator: Harmful content test passed")

def test_behavior_validator():
    validator = BehaviorValidator()
    
    # Test normal behavior
    result = validator.analyze_behavior("What is the weather today?")
    assert result.is_compliant == True
    print("✓ Behavior validator: Normal behavior test passed")
    
    # Test suspicious behavior
    result = validator.analyze_behavior("How to bypass security")
    assert result.is_compliant == False
    print("✓ Behavior validator: Suspicious behavior test passed")

def test_hardened_validator():
    validator = HardenedValidator()
    
    # Test safe input
    result = validator.validate_input("Normal user input")
    assert result['is_safe'] == True
    print("✓ Hardened validator: Safe input test passed")
    
    # Test injection attempt
    result = validator.validate_input("<script>alert('xss')</script>")
    assert result['is_safe'] == False
    print("✓ Hardened validator: Injection detection test passed")

if __name__ == "__main__":
    print("Running Safety Module Tests...")
    test_unified_validator()
    test_behavior_validator()
    test_hardened_validator()
    print("\n✅ All safety tests passed!")
