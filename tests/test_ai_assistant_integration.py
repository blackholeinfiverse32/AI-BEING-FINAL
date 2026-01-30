"""
Test AI-ASSISTANT Integration
Validates all components integrated from AI-ASSISTANT repository
"""
import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

import asyncio

def test_agents_import():
    """Test that all agents can be imported"""
    print("Testing agents import...")
    from core.agents import (
        BaseAgent, PlannerAgent, ResearcherAgent,
        AnalystAgent, EvaluatorAgent, ExecutorAgent
    )
    print("  [OK] All agents imported successfully")
    return True

def test_bhiv_integration():
    """Test BHIV integration"""
    print("Testing BHIV integration...")
    from intelligence_layer.bhiv_integration import BHIVCore, BHIVReasoner, create_bhiv_system
    print("  [OK] BHIV modules imported successfully")
    return True

def test_karma_system():
    """Test Karma system"""
    print("Testing Karma system...")
    from intelligence_layer.karma_system import KarmaSystem, karma_system, karma_hook
    
    # Test karma tracking
    result = karma_hook("test_user", "test_action", 15)
    assert result["karma_points"] == 15
    assert result["user_id"] == "test_user"
    
    # Test karma retrieval
    karma = karma_system.get_karma("test_user")
    assert karma["total_karma"] == 15
    
    # Test karma level
    level = karma_system.get_karma_level("test_user")
    assert level == "novice"
    
    print("  [OK] Karma system working correctly")
    return True

def test_insight_engine():
    """Test Insight engine"""
    print("Testing Insight engine...")
    from intelligence_layer.insight_engine import InsightEngine, insight_engine, insightflow_hook
    
    # Log interactions
    insightflow_hook("user1", "test query 1", "result 1")
    insightflow_hook("user1", "test query 2", "result 2")
    insightflow_hook("user2", "test query 3", "result 3")
    
    # Generate user insights
    insights = insight_engine.generate_user_insights("user1")
    assert insights["total_interactions"] == 2
    
    # Generate system insights
    system_insights = insight_engine.generate_system_insights()
    assert system_insights["unique_users"] == 2
    
    print("  [OK] Insight engine working correctly")
    return True

def test_calculator_tool():
    """Test Calculator tool"""
    print("Testing Calculator tool...")
    from tools.calculator_tool import CalculatorTool, calculator_tool
    
    calc = CalculatorTool()
    
    # Test basic calculation
    result = asyncio.run(calc.run("2 + 2"))
    assert "4" in result
    
    # Test multiplication
    result = asyncio.run(calc.run("5 * 3"))
    assert "15" in result
    
    # Test division
    result = asyncio.run(calc.run("10 / 2"))
    assert "5" in result
    
    # Test error handling
    result = asyncio.run(calc.run("10 / 0"))
    assert "Error" in result or "zero" in result.lower()
    
    print("  [OK] Calculator tool working correctly")
    return True

def test_llm_router_mistral():
    """Test LLM router with Mistral support"""
    print("Testing LLM router Mistral support...")
    from core.llm_router import LLMRouter, LLMProvider
    
    router = LLMRouter()
    
    # Check if Mistral is in providers enum
    assert hasattr(LLMProvider, 'MISTRAL')
    assert LLMProvider.MISTRAL.value == "mistral"
    
    print("  [OK] Mistral support added to LLM router")
    return True

async def test_agent_workflow():
    """Test agent workflow"""
    print("Testing agent workflow...")
    from core.agents import PlannerAgent, ResearcherAgent, AnalystAgent, ExecutorAgent, EvaluatorAgent
    
    # Create agents
    planner = PlannerAgent()
    researcher = ResearcherAgent()
    analyst = AnalystAgent()
    executor = ExecutorAgent()
    evaluator = EvaluatorAgent()
    
    # Test planner
    plan = await planner.run("test query", {})
    assert plan["agent"] == "planner"
    assert "steps" in plan["output"]
    
    # Test researcher
    research = await researcher.run("test task", {})
    assert research["agent"] == "researcher"
    
    # Test analyst
    analysis = await analyst.run("test data", {})
    assert analysis["agent"] == "analyst"
    
    # Test executor
    execution = await executor.run("test action", {})
    assert execution["agent"] == "executor"
    
    # Test evaluator
    evaluation = await evaluator.run([plan, research], {})
    assert evaluation["agent"] == "evaluator"
    
    print("  [OK] Agent workflow working correctly")
    return True

async def test_bhiv_workflow():
    """Test BHIV workflow"""
    print("Testing BHIV workflow...")
    from intelligence_layer.bhiv_integration import create_bhiv_system
    from core.memory_manager import MemoryManager
    from core.agents import PlannerAgent, ResearcherAgent, AnalystAgent, ExecutorAgent, EvaluatorAgent
    
    # Create memory manager
    memory = MemoryManager()
    
    # Create agents
    agents = {
        "planner": PlannerAgent(),
        "researcher": ResearcherAgent(),
        "analyst": AnalystAgent(),
        "executor": ExecutorAgent(),
        "evaluator": EvaluatorAgent()
    }
    
    # Create BHIV system
    bhiv = create_bhiv_system(memory, agents, {})
    
    # Process input
    result = await bhiv.process({"user_id": "test_user", "query": "test query"})
    assert result is not None
    
    print("  [OK] BHIV workflow working correctly")
    return True

def run_all_tests():
    """Run all integration tests"""
    print("=" * 60)
    print("AI-ASSISTANT Integration Tests")
    print("=" * 60)
    print()
    
    tests = [
        ("Agents Import", test_agents_import),
        ("BHIV Integration", test_bhiv_integration),
        ("Karma System", test_karma_system),
        ("Insight Engine", test_insight_engine),
        ("Calculator Tool", test_calculator_tool),
        ("LLM Router Mistral", test_llm_router_mistral),
    ]
    
    async_tests = [
        ("Agent Workflow", test_agent_workflow),
        ("BHIV Workflow", test_bhiv_workflow),
    ]
    
    passed = 0
    failed = 0
    
    # Run synchronous tests
    for name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"  [FAIL] {name}: {e}")
            failed += 1
        print()
    
    # Run asynchronous tests
    for name, test_func in async_tests:
        try:
            if asyncio.run(test_func()):
                passed += 1
        except Exception as e:
            print(f"  [FAIL] {name}: {e}")
            failed += 1
        print()
    
    print("=" * 60)
    print(f"Results: {passed} passed, {failed} failed")
    print("=" * 60)
    
    if failed == 0:
        print("\n[SUCCESS] All AI-ASSISTANT integration tests passed!")
        print("\nIntegrated Components:")
        print("  - 6 Specialized Agents (Planner, Researcher, Analyst, Evaluator, Executor, Base)")
        print("  - BHIV Intelligence Core & Reasoner")
        print("  - Karma System (user behavior tracking)")
        print("  - Insight Engine (analytics & learning)")
        print("  - Calculator Tool (mathematical operations)")
        print("  - Mistral LLM Support")
        return True
    else:
        print(f"\n[FAILURE] {failed} test(s) failed")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
