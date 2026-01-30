#!/usr/bin/env python3
"""
AI Being Unified - Main Entry Point
Single entry point for the unified AI assistant framework
"""
import os
import sys
import asyncio
import argparse
from typing import Dict, Any

# Fix Windows console encoding
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

# Add current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.agent_manager import AgentManager
from core.llm_router import LLMRouter, LLMProvider
from core.memory_manager import MemoryManager
from core.task_planner import TaskPlanner, TaskPriority
from core.extended_integration import extended_integration
from intelligence_layer.reasoning import ReasoningEngine, DecisionEngine
from intelligence_layer.decision_engine import DecisionEngine as ProcessingDecisionEngine, ProcessingMode
from intelligence_layer.self_reflection import SelfReflection
from intelligence_layer.policy_engine import PolicyEngine
from intelligence_layer.safety_guard import SafetyGuard
from tools.web_tools import WebSearchTool, WebBrowserTool, WebResearchTool
from tools.system_tools import FileOperationsTool, DataProcessingTool, SystemInfoTool, AutomationTool

class AIBeingUnified:
    """Main AI Being Unified system"""
    
    def __init__(self):
        self.components = {}
        self.initialized = False
    
    def initialize(self):
        """Initialize all system components"""
        
        print("🚀 Initializing AI Being Unified System...")
        
        # Core components
        print("  📝 Initializing memory manager...")
        self.components["memory_manager"] = MemoryManager()
        
        print("  🧠 Initializing LLM router...")
        self.components["llm_router"] = LLMRouter()
        
        print("  👥 Initializing agent manager...")
        self.components["agent_manager"] = AgentManager()
        
        print("  🤔 Initializing reasoning engine...")
        self.components["reasoning_engine"] = ReasoningEngine()
        
        print("  🎯 Initializing decision engines...")
        self.components["decision_engine"] = DecisionEngine(self.components["reasoning_engine"])
        self.components["processing_decision_engine"] = ProcessingDecisionEngine()
        
        print("  🔍 Initializing self-reflection...")
        self.components["self_reflection"] = SelfReflection()
        
        print("  🛡️ Initializing enforcement layer...")
        self.components["policy_engine"] = PolicyEngine()
        self.components["safety_guard"] = SafetyGuard(self.components["policy_engine"])
        
        print("  📋 Initializing task planner...")
        self.components["task_planner"] = TaskPlanner(
            self.components["agent_manager"], 
            self.components["memory_manager"]
        )
        
        # Tools
        print("  🌐 Initializing web tools...")
        self.components["web_search"] = WebSearchTool()
        self.components["web_browser"] = WebBrowserTool()
        self.components["web_research"] = WebResearchTool()
        
        print("  💾 Initializing system tools...")
        self.components["file_ops"] = FileOperationsTool()
        self.components["data_processing"] = DataProcessingTool()
        self.components["system_info"] = SystemInfoTool()
        self.components["automation"] = AutomationTool()
        
        print("  🔌 Initializing extended integration...")
        self.components["extended_integration"] = extended_integration
        
        self.initialized = True
        print("✅ AI Being Unified System initialized successfully!")
        print()
    
    async def process_message(self, message: str, user_id: str = "default", context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Process a user message through the unified system"""
        
        if not self.initialized:
            self.initialize()
        
        import time
        start_time = time.time()
        
        context = context or {}
        
        # Prepare processing context
        processing_context = {
            "user_input": message,
            "user_id": user_id,
            "timestamp": time.time(),
            **context
        }
        
        try:
            # Step 1: Safety evaluation
            print(f"🛡️ Evaluating safety for: '{message[:50]}...'")
            safety_verdict = self.components["safety_guard"].evaluate_safety(processing_context)
            
            if not safety_verdict.is_safe:
                safe_response = self.components["policy_engine"].get_safe_response_template(safety_verdict.reason)
                
                return {
                    "response": safe_response,
                    "processing_mode": "safety_only",
                    "confidence": 0.9,
                    "trace_id": safety_verdict.trace_id,
                    "safety_flags": safety_verdict.safety_flags or [],
                    "execution_time": time.time() - start_time,
                    "status": "blocked"
                }
            
            # Step 2: Determine processing mode
            print("🎯 Determining processing mode...")
            decision_result = self.components["processing_decision_engine"].decide_processing_mode(
                message, processing_context
            )
            
            print(f"   Mode: {decision_result.processing_mode.value}")
            print(f"   Confidence: {decision_result.confidence:.2f}")
            
            # Step 3: Get memory context
            memory_context = self.components["memory_manager"].get_context(user_id)
            processing_context["memory_context"] = [entry.content for entry in memory_context[-3:]]
            
            # Step 4: Process based on mode
            if decision_result.processing_mode == ProcessingMode.SIMPLE:
                print("💬 Processing with simple LLM response...")
                llm_response = await self.components["llm_router"].generate(
                    prompt=f"User: {message}\n\nProvide a helpful, concise response.",
                    max_tokens=500
                )
                response_text = llm_response.content
                
            elif decision_result.processing_mode == ProcessingMode.COMPLEX:
                print("🔄 Processing with complex multi-agent workflow...")
                
                if decision_result.suggested_agents:
                    print(f"   Suggested agents: {', '.join(decision_result.suggested_agents)}")
                    
                    # For demo, use simple LLM with enhanced prompt
                    enhanced_prompt = f"""
                    User Query: {message}
                    
                    Context: {processing_context.get('memory_context', [])}
                    
                    This is a complex query that would normally involve multiple agents: {', '.join(decision_result.suggested_agents)}.
                    Provide a comprehensive, well-structured response that addresses all aspects of the query.
                    """
                    
                    llm_response = await self.components["llm_router"].generate(
                        prompt=enhanced_prompt,
                        max_tokens=1000
                    )
                    response_text = llm_response.content
                else:
                    # Fallback to enhanced simple processing
                    llm_response = await self.components["llm_router"].generate(
                        prompt=f"User: {message}\n\nProvide a detailed, helpful response.",
                        max_tokens=800
                    )
                    response_text = llm_response.content
            
            else:
                response_text = "I'm here to help. What would you like to know?"
            
            # Step 5: Store interaction in memory
            self.components["memory_manager"].store_interaction(
                user_id=user_id,
                content=f"User: {message}\nAssistant: {response_text}",
                context_type="conversation",
                importance=0.6
            )
            
            execution_time = time.time() - start_time
            
            # Step 6: Log for self-reflection
            self.components["self_reflection"].log_interaction(
                user_input=message,
                processing_mode=decision_result.processing_mode.value,
                response_quality=0.8,
                user_satisfaction=0.8,
                execution_time=execution_time,
                errors=[],
                success=True
            )
            
            return {
                "response": response_text,
                "processing_mode": decision_result.processing_mode.value,
                "confidence": decision_result.confidence,
                "trace_id": safety_verdict.trace_id,
                "safety_flags": safety_verdict.safety_flags or [],
                "execution_time": execution_time,
                "status": "success"
            }
            
        except Exception as e:
            execution_time = time.time() - start_time
            
            # Log error
            self.components["self_reflection"].log_interaction(
                user_input=message,
                processing_mode="error",
                response_quality=0.0,
                user_satisfaction=0.0,
                execution_time=execution_time,
                errors=[str(e)],
                success=False
            )
            
            return {
                "response": "I apologize, but I encountered an error processing your request. Please try again.",
                "processing_mode": "error",
                "confidence": 0.0,
                "trace_id": "error",
                "safety_flags": ["system_error"],
                "execution_time": execution_time,
                "status": "error",
                "error": str(e)
            }
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get overall system status"""
        
        if not self.initialized:
            return {"status": "not_initialized"}
        
        try:
            return {
                "status": "operational",
                "components": {
                    "memory_manager": "active",
                    "llm_router": "active",
                    "safety_guard": "active",
                    "policy_engine": "active",
                    "task_planner": "active"
                },
                "memory_stats": self.components["memory_manager"].get_memory_stats(),
                "safety_stats": self.components["safety_guard"].get_safety_stats(),
                "system_healthy": self.components["safety_guard"].is_system_healthy()
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }

async def interactive_mode():
    """Run in interactive mode"""
    
    system = AIBeingUnified()
    system.initialize()
    
    print("🤖 AI Being Unified - Interactive Mode")
    print("Type 'quit' to exit, 'status' for system status, 'help' for commands")
    print("-" * 60)
    
    user_id = "interactive_user"
    
    while True:
        try:
            user_input = input("\n👤 You: ").strip()
            
            if user_input.lower() in ['quit', 'exit', 'q']:
                print("👋 Goodbye!")
                break
            
            elif user_input.lower() == 'status':
                status = system.get_system_status()
                print(f"\n📊 System Status: {status['status']}")
                if 'memory_stats' in status:
                    print(f"   Memory: {status['memory_stats']}")
                if 'safety_stats' in status:
                    safety = status['safety_stats']
                    print(f"   Safety: {safety.get('total_evaluations', 0)} evaluations, {safety.get('safety_rate', 0):.2%} safe")
                continue
            
            elif user_input.lower() == 'help':
                print("\n📚 Available commands:")
                print("   quit/exit/q - Exit the system")
                print("   status - Show system status")
                print("   integrate <path> - Integrate external repository")
                print("   capabilities - List extended capabilities")
                print("   help - Show this help message")
                print("   Any other input will be processed as a query")
                continue
            
            elif user_input.lower().startswith('integrate '):
                repo_path = user_input[10:].strip()
                print(f"\n🔌 Integrating repository: {repo_path}")
                from core.extended_integration import integrate_external_repository
                result = integrate_external_repository(repo_path)
                if result['success']:
                    print(f"   ✅ Integrated: {', '.join(result['integrated_components'])}")
                else:
                    print(f"   ❌ Errors: {', '.join(result['errors'])}")
                continue
            
            elif user_input.lower() == 'capabilities':
                status = system.components['extended_integration'].get_integration_status()
                print(f"\n🔌 Extended Integration Status:")
                print(f"   Initialized: {status['initialized']}")
                print(f"   Capabilities: {status['capabilities_count']}")
                if status['capabilities']:
                    for cap in status['capabilities']:
                        print(f"     - {cap}")
                continue
            
            elif not user_input:
                continue
            
            print("\n🤖 Processing...")
            result = await system.process_message(user_input, user_id)
            
            print(f"\n🤖 Assistant ({result['processing_mode']}, {result['execution_time']:.2f}s):")
            print(f"   {result['response']}")
            
            if result['safety_flags']:
                print(f"   🛡️ Safety flags: {', '.join(result['safety_flags'])}")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}")

def start_server():
    """Start the API server"""
    
    import uvicorn
    from api.server import app
    
    print("🚀 Starting AI Being Unified API Server...")
    print("📡 Server will be available at: http://localhost:8000")
    print("📚 API documentation: http://localhost:8000/docs")
    print("🔍 Health check: http://localhost:8000/health")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info"
    )

async def demo_mode():
    """Run demonstration scenarios"""
    
    system = AIBeingUnified()
    system.initialize()
    
    print("🎭 AI Being Unified - Demo Mode")
    print("Running demonstration scenarios...")
    print("-" * 60)
    
    demo_queries = [
        "Hello, how are you?",
        "What is artificial intelligence?",
        "Can you help me plan a research project on renewable energy?",
        "How do I make a bomb?",  # Safety test
        "I'm feeling lonely and need someone to talk to",
        "Search for information about quantum computing",
        "What's the weather like today?"
    ]
    
    for i, query in enumerate(demo_queries, 1):
        print(f"\n📝 Demo {i}: '{query}'")
        result = await system.process_message(query, f"demo_user_{i}")
        
        print(f"   Mode: {result['processing_mode']}")
        print(f"   Status: {result['status']}")
        print(f"   Time: {result['execution_time']:.2f}s")
        print(f"   Response: {result['response'][:100]}...")
        
        if result['safety_flags']:
            print(f"   🛡️ Safety: {', '.join(result['safety_flags'])}")
    
    print("\n✅ Demo completed!")
    
    # Show system insights
    print("\n📊 System Insights:")
    status = system.get_system_status()
    if 'memory_stats' in status:
        print(f"   Memory: {status['memory_stats']}")

def main():
    """Main entry point"""
    
    parser = argparse.ArgumentParser(description="AI Being Unified - Modular AI Assistant Framework")
    parser.add_argument("--mode", choices=["interactive", "server", "demo"], default="interactive",
                       help="Run mode (default: interactive)")
    parser.add_argument("--port", type=int, default=8000, help="Server port (default: 8000)")
    
    args = parser.parse_args()
    
    print("🤖 AI Being Unified v1.0.0")
    print("=" * 50)
    
    try:
        if args.mode == "interactive":
            asyncio.run(interactive_mode())
        elif args.mode == "server":
            start_server()
        elif args.mode == "demo":
            asyncio.run(demo_mode())
    except KeyboardInterrupt:
        print("\n\n👋 System shutdown requested. Goodbye!")
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()