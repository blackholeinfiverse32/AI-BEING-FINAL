"""Audit Mode - Comprehensive System Verification"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import json
from datetime import datetime

def run_audit():
    """Run comprehensive system audit"""
    
    audit_results = {
        "timestamp": datetime.now().isoformat(),
        "agents": "UNKNOWN",
        "reasoning": "UNKNOWN",
        "enforcement": "UNKNOWN",
        "tools": "UNKNOWN",
        "memory": "UNKNOWN",
        "api": "UNKNOWN",
        "llm_router": "UNKNOWN",
        "extended_integration": "UNKNOWN",
        "repo_coverage": "0%",
        "details": {},
        "failures": []
    }
    
    print("\n" + "="*70)
    print("AI BEING UNIFIED - SYSTEM AUDIT")
    print("="*70 + "\n")
    
    # Test 1: Agent Manager
    try:
        from core.agent_manager import AgentManager
        manager = AgentManager()
        audit_results["agents"] = "OK"
        audit_results["details"]["agents"] = "AgentManager loaded successfully"
        print("[OK] Agent Manager")
    except Exception as e:
        audit_results["agents"] = "FAIL"
        audit_results["failures"].append(f"Agent Manager: {e}")
        print(f"[FAIL] Agent Manager: {e}")
    
    # Test 2: Reasoning Engine
    try:
        from intelligence_layer.reasoning import ReasoningEngine
        engine = ReasoningEngine()
        output, _ = engine.process_interaction({"user_age": 25}, {}, {})
        assert "behavioral_state" in output
        audit_results["reasoning"] = "OK"
        audit_results["details"]["reasoning"] = "ReasoningEngine functional"
        print("[OK] Reasoning Engine")
    except Exception as e:
        audit_results["reasoning"] = "FAIL"
        audit_results["failures"].append(f"Reasoning: {e}")
        print(f"[FAIL] Reasoning Engine: {e}")
    
    # Test 3: Enforcement
    try:
        from enforcement.policy_engine import PolicyEngine
        from enforcement.safety_guard import SafetyGuard
        policy = PolicyEngine()
        guard = SafetyGuard(policy)
        verdict = guard.evaluate_safety({"user_input": "test", "user_age": 25})
        assert verdict is not None
        audit_results["enforcement"] = "OK"
        audit_results["details"]["enforcement"] = "Policy & Safety Guard active"
        print("[OK] Enforcement Layer")
    except Exception as e:
        audit_results["enforcement"] = "FAIL"
        audit_results["failures"].append(f"Enforcement: {e}")
        print(f"[FAIL] Enforcement: {e}")
    
    # Test 4: Tools
    try:
        from tools.web_tools import WebSearchTool
        from tools.system_tools import FileOperationsTool
        search = WebSearchTool()
        files = FileOperationsTool()
        audit_results["tools"] = "OK"
        audit_results["details"]["tools"] = "Web & System tools loaded"
        print("[OK] Tools")
    except Exception as e:
        audit_results["tools"] = "FAIL"
        audit_results["failures"].append(f"Tools: {e}")
        print(f"[FAIL] Tools: {e}")
    
    # Test 5: Memory
    try:
        from core.memory_manager import MemoryManager
        memory = MemoryManager()
        stats = memory.get_memory_stats()
        audit_results["memory"] = "OK"
        audit_results["details"]["memory"] = f"Memory stats: {stats}"
        print("[OK] Memory Manager")
    except Exception as e:
        audit_results["memory"] = "FAIL"
        audit_results["failures"].append(f"Memory: {e}")
        print(f"[FAIL] Memory: {e}")
    
    # Test 6: LLM Router
    try:
        from core.llm_router import LLMRouter
        router = LLMRouter()
        audit_results["llm_router"] = "OK"
        audit_results["details"]["llm_router"] = f"Providers: {len(router.providers)}"
        print("[OK] LLM Router")
    except Exception as e:
        audit_results["llm_router"] = "FAIL"
        audit_results["failures"].append(f"LLM Router: {e}")
        print(f"[FAIL] LLM Router: {e}")
    
    # Test 7: API
    try:
        from api.server import app
        audit_results["api"] = "OK"
        audit_results["details"]["api"] = "FastAPI app loaded"
        print("[OK] API Server")
    except Exception as e:
        audit_results["api"] = "FAIL"
        audit_results["failures"].append(f"API: {e}")
        print(f"[FAIL] API: {e}")
    
    # Test 8: Extended Integration
    try:
        from core.extended_integration import extended_integration
        status = extended_integration.get_integration_status()
        audit_results["extended_integration"] = "OK"
        audit_results["details"]["extended_integration"] = status
        print("[OK] Extended Integration")
    except Exception as e:
        audit_results["extended_integration"] = "FAIL"
        audit_results["failures"].append(f"Extended Integration: {e}")
        print(f"[FAIL] Extended Integration: {e}")
    
    # Calculate coverage
    total_components = 8
    passed_components = sum(1 for v in [
        audit_results["agents"],
        audit_results["reasoning"],
        audit_results["enforcement"],
        audit_results["tools"],
        audit_results["memory"],
        audit_results["llm_router"],
        audit_results["api"],
        audit_results["extended_integration"]
    ] if v == "OK")
    
    audit_results["repo_coverage"] = f"{(passed_components/total_components)*100:.0f}%"
    
    print("\n" + "="*70)
    print("AUDIT SUMMARY")
    print("="*70)
    print(f"Coverage: {audit_results['repo_coverage']}")
    print(f"Passed: {passed_components}/{total_components}")
    
    if audit_results["failures"]:
        print("\nFAILURES:")
        for failure in audit_results["failures"]:
            print(f"  - {failure}")
    
    print("="*70 + "\n")
    
    # Save audit report
    with open("audit_report.json", "w") as f:
        json.dump(audit_results, f, indent=2)
    
    print(f"Audit report saved to: audit_report.json\n")
    
    return audit_results

if __name__ == "__main__":
    results = run_audit()
    sys.exit(0 if results["repo_coverage"] == "100%" else 1)
