"""Reasoning Engine Verification Tests"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from intelligence_layer.reasoning import ReasoningEngine

def test_reasoning_engine():
    print("Testing Reasoning Engine...")
    engine = ReasoningEngine()
    context = {"user_age": 25, "region": "US"}
    karma = {"karma_score": 80, "risk_signal": "low"}
    bucket = {"baseline_emotional_band": "neutral"}
    output, bucket_write = engine.process_interaction(context, karma, bucket)
    assert "behavioral_state" in output
    assert "trace_id" in output
    assert "safe_mode" in output
    print("[PASS] Reasoning Engine")
    return True

def test_minor_detection():
    print("Testing Minor Detection...")
    engine = ReasoningEngine()
    context = {"user_age": 15, "region": "US"}
    output, _ = engine.process_interaction(context)
    assert output["safe_mode"] == "on"
    assert "minor_detected" in output["constraints"]["gating_flags"]
    print("[PASS] Minor Detection")
    return True

if __name__ == "__main__":
    print("\n" + "="*60)
    print("REASONING VERIFICATION TESTS")
    print("="*60 + "\n")
    results = [test_reasoning_engine(), test_minor_detection()]
    print("\n" + "="*60)
    print(f"RESULT: {sum(results)}/{len(results)} PASS")
    print("="*60 + "\n")
    sys.exit(0 if all(results) else 1)
