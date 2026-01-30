"""Agent Verification Tests"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import asyncio
from core.agent_manager import AgentManager, AgentResult

class MockAgent:
    async def process(self, task_data):
        return {"status": "success", "data": task_data.get("input", "processed")}

async def test_agent_manager():
    print("Testing Agent Manager...")
    manager = AgentManager()
    manager.register_agent("test_agent", MockAgent())
    result = await manager.execute_agent("test_agent", {"input": "test_data"})
    assert isinstance(result, AgentResult)
    assert result.agent_name == "test_agent"
    assert result.result["status"] == "success"
    print("[PASS] Agent Manager")
    return True

async def run_all():
    print("\n" + "="*60)
    print("AGENT VERIFICATION TESTS")
    print("="*60 + "\n")
    result = await test_agent_manager()
    print("\n" + "="*60)
    print(f"RESULT: {'PASS' if result else 'FAIL'}")
    print("="*60 + "\n")
    return result

if __name__ == "__main__":
    success = asyncio.run(run_all())
    sys.exit(0 if success else 1)
