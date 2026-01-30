"""Enforcement Module Tests"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from backend.enforcement.enforcement_engine import EnforcementEngine
from backend.enforcement.enforcement_gateway import EnforcementGateway
from backend.enforcement.executor_runtime import ExecutorRuntime

def test_enforcement_engine():
    engine = EnforcementEngine()
    
    context = {'harmful_detected': True}
    result = engine.evaluate(context)
    assert result['action'] == 'block'
    print("✓ Enforcement engine: Block action test passed")

def test_enforcement_gateway():
    gateway = EnforcementGateway()
    
    result = gateway.check_request('user123', {'message': 'Hello world'})
    assert 'allowed' in result
    print("✓ Enforcement gateway: Request check test passed")

def test_executor_runtime():
    runtime = ExecutorRuntime()
    
    result = runtime.execute('allow', {'data': 'test'})
    assert result['status'] == 'allowed'
    print("✓ Executor runtime: Execution test passed")

if __name__ == "__main__":
    print("Running Enforcement Module Tests...")
    test_enforcement_engine()
    test_enforcement_gateway()
    test_executor_runtime()
    print("\n✅ All enforcement tests passed!")
