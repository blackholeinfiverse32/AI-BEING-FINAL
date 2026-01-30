"""
AI Being Unified - API Server
FastAPI server providing unified AI assistant capabilities
"""
import os
import sys
from datetime import datetime
from contextlib import asynccontextmanager
from typing import Dict, Any, Optional, List

from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field
import uvicorn
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.agent_manager import AgentManager
from core.llm_router import LLMRouter, LLMProvider
from core.memory_manager import MemoryManager
from core.task_planner import TaskPlanner, TaskPriority
from intelligence_layer.reasoning import ReasoningEngine, DecisionEngine
from intelligence_layer.decision_engine import DecisionEngine as ProcessingDecisionEngine, ProcessingMode
from intelligence_layer.self_reflection import SelfReflection
from intelligence_layer.policy_engine import PolicyEngine
from intelligence_layer.safety_guard import SafetyGuard
from tools.web_tools import WebSearchTool, WebBrowserTool, WebResearchTool
from tools.system_tools import FileOperationsTool, DataProcessingTool, SystemInfoTool, AutomationTool

# Pydantic models for API
class ChatRequest(BaseModel):
    message: str = Field(..., description="User message")
    user_id: str = Field(default="anonymous", description="User identifier")
    session_id: str = Field(default="default", description="Session identifier")
    context: Dict[str, Any] = Field(default_factory=dict, description="Additional context")

class ChatResponse(BaseModel):
    response: str
    processing_mode: str
    confidence: float
    trace_id: str
    safety_flags: List[str] = Field(default_factory=list)
    execution_time: float

class TaskRequest(BaseModel):
    name: str
    description: str
    agents: List[str]
    input_data: Dict[str, Any] = Field(default_factory=dict)
    priority: str = Field(default="medium")

class SearchRequest(BaseModel):
    query: str
    max_results: int = Field(default=5, ge=1, le=20)

class FileRequest(BaseModel):
    file_path: str
    content: Optional[str] = None
    operation: str  # read, write, delete, list

# Global components
components = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize and cleanup application components"""
    
    # Initialize core components
    components["memory_manager"] = MemoryManager()
    components["llm_router"] = LLMRouter()
    components["agent_manager"] = AgentManager()
    components["reasoning_engine"] = ReasoningEngine()
    components["decision_engine"] = DecisionEngine(components["reasoning_engine"])
    components["processing_decision_engine"] = ProcessingDecisionEngine()
    components["self_reflection"] = SelfReflection()
    components["policy_engine"] = PolicyEngine()
    components["safety_guard"] = SafetyGuard(components["policy_engine"])
    components["task_planner"] = TaskPlanner(components["agent_manager"], components["memory_manager"])
    
    # Initialize tools
    components["web_search"] = WebSearchTool()
    components["web_browser"] = WebBrowserTool()
    components["web_research"] = WebResearchTool()
    components["file_ops"] = FileOperationsTool()
    components["data_processing"] = DataProcessingTool()
    components["system_info"] = SystemInfoTool()
    components["automation"] = AutomationTool()
    
    print("AI Being Unified system initialized successfully")
    yield
    
    # Cleanup
    print("AI Being Unified system shutting down")

# Create FastAPI app
app = FastAPI(
    title="AI Being Unified",
    description="Unified AI Assistant Framework",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Key authentication
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)

def verify_api_key(api_key: str = Depends(api_key_header)):
    """Verify API key"""
    expected_key = os.getenv("API_KEY", "ai_being_unified_demo_key")
    if api_key != expected_key:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return api_key

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0",
        "components": {
            "memory_manager": "active",
            "llm_router": "active",
            "safety_guard": "active",
            "policy_engine": "active"
        }
    }

# Main chat endpoint
@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, api_key: str = Depends(verify_api_key)):
    """Main chat endpoint for AI assistant"""
    
    import time
    start_time = time.time()
    
    try:
        # Prepare context for processing
        context = {
            "user_input": request.message,
            "user_id": request.user_id,
            "session_id": request.session_id,
            "timestamp": datetime.now().isoformat(),
            **request.context
        }
        
        # Safety evaluation first
        safety_verdict = components["safety_guard"].evaluate_safety(context)
        
        if not safety_verdict.is_safe:
            # Return safe response for blocked content
            safe_response = components["policy_engine"].get_safe_response_template(safety_verdict.reason)
            
            execution_time = time.time() - start_time
            
            # Log interaction for self-reflection
            components["self_reflection"].log_interaction(
                user_input=request.message,
                processing_mode="safety_only",
                response_quality=0.8,
                user_satisfaction=0.5,  # Neutral for safety blocks
                execution_time=execution_time,
                errors=[],
                success=True
            )
            
            return ChatResponse(
                response=safe_response,
                processing_mode="safety_only",
                confidence=0.9,
                trace_id=safety_verdict.trace_id,
                safety_flags=safety_verdict.safety_flags or [],
                execution_time=execution_time
            )
        
        # Determine processing mode
        decision_result = components["processing_decision_engine"].decide_processing_mode(
            request.message, context
        )
        
        # Get user memory context
        memory_context = components["memory_manager"].get_context(request.user_id)
        context["memory_context"] = [entry.content for entry in memory_context[-5:]]  # Last 5 entries
        
        # Process based on decision
        if decision_result.processing_mode == ProcessingMode.SIMPLE:
            # Simple LLM response
            llm_response = await components["llm_router"].generate(
                prompt=f"User: {request.message}\n\nProvide a helpful, concise response.",
                max_tokens=500
            )
            response_text = llm_response.content
            
        elif decision_result.processing_mode == ProcessingMode.COMPLEX:
            # Complex multi-agent processing
            if decision_result.suggested_agents:
                # Create and execute task
                task_id = components["task_planner"].create_workflow_task(
                    workflow_steps=decision_result.suggested_agents,
                    input_data={"user_input": request.message, "context": context},
                    name="Complex Query Processing"
                )
                
                task_result = await components["task_planner"].execute_task(task_id)
                
                if task_result.status.value == "completed":
                    response_text = str(task_result.result.get("final_result", "Task completed successfully"))
                else:
                    response_text = "I encountered some difficulties processing your request. Let me try a simpler approach."
                    # Fallback to simple processing
                    llm_response = await components["llm_router"].generate(
                        prompt=f"User: {request.message}\n\nProvide a helpful response.",
                        max_tokens=500
                    )
                    response_text = llm_response.content
            else:
                # Fallback to simple processing
                llm_response = await components["llm_router"].generate(
                    prompt=f"User: {request.message}\n\nProvide a helpful, detailed response.",
                    max_tokens=800
                )
                response_text = llm_response.content
        
        else:
            response_text = "I'm here to help. What would you like to know?"
        
        # Store interaction in memory
        components["memory_manager"].store_interaction(
            user_id=request.user_id,
            content=f"User: {request.message}\nAssistant: {response_text}",
            context_type="conversation",
            importance=0.6
        )
        
        execution_time = time.time() - start_time
        
        # Log interaction for self-reflection
        components["self_reflection"].log_interaction(
            user_input=request.message,
            processing_mode=decision_result.processing_mode.value,
            response_quality=0.8,
            user_satisfaction=0.8,  # Default assumption
            execution_time=execution_time,
            errors=[],
            success=True
        )
        
        return ChatResponse(
            response=response_text,
            processing_mode=decision_result.processing_mode.value,
            confidence=decision_result.confidence,
            trace_id=safety_verdict.trace_id,
            safety_flags=safety_verdict.safety_flags or [],
            execution_time=execution_time
        )
        
    except Exception as e:
        execution_time = time.time() - start_time
        
        # Log error for self-reflection
        components["self_reflection"].log_interaction(
            user_input=request.message,
            processing_mode="error",
            response_quality=0.0,
            user_satisfaction=0.0,
            execution_time=execution_time,
            errors=[str(e)],
            success=False
        )
        
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

# Task management endpoints
@app.post("/api/tasks")
async def create_task(request: TaskRequest, api_key: str = Depends(verify_api_key)):
    """Create a new task"""
    
    try:
        priority_map = {
            "low": TaskPriority.LOW,
            "medium": TaskPriority.MEDIUM,
            "high": TaskPriority.HIGH,
            "critical": TaskPriority.CRITICAL
        }
        
        priority = priority_map.get(request.priority.lower(), TaskPriority.MEDIUM)
        
        # Create task steps
        steps = []
        for i, agent in enumerate(request.agents):
            steps.append({
                "agent": agent,
                "input": request.input_data if i == 0 else {},
                "dependencies": [f"step_{i-1}"] if i > 0 else []
            })
        
        task_id = components["task_planner"].create_task(
            name=request.name,
            description=request.description,
            steps=steps,
            priority=priority
        )
        
        return {"task_id": task_id, "status": "created"}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/tasks/{task_id}")
async def get_task_status(task_id: str, api_key: str = Depends(verify_api_key)):
    """Get task status"""
    
    task = components["task_planner"].get_task_status(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return {
        "task_id": task.task_id,
        "name": task.name,
        "status": task.status.value,
        "result": task.result
    }

# Search endpoints
@app.post("/api/search")
async def web_search(request: SearchRequest, api_key: str = Depends(verify_api_key)):
    """Web search endpoint"""
    
    try:
        results = components["web_search"].search(request.query, request.max_results)
        
        return {
            "query": request.query,
            "results": [
                {
                    "title": result.title,
                    "url": result.url,
                    "snippet": result.snippet,
                    "relevance": result.relevance_score
                }
                for result in results
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/research")
async def web_research(request: SearchRequest, api_key: str = Depends(verify_api_key)):
    """Web research endpoint"""
    
    try:
        research_results = components["web_research"].research_topic(
            request.query, 
            depth=min(request.max_results, 5)
        )
        
        return research_results
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# File operations endpoints
@app.post("/api/files")
async def file_operations(request: FileRequest, api_key: str = Depends(verify_api_key)):
    """File operations endpoint"""
    
    try:
        if request.operation == "read":
            result = components["file_ops"].read_file(request.file_path)
        elif request.operation == "write":
            if not request.content:
                raise HTTPException(status_code=400, detail="Content required for write operation")
            result = components["file_ops"].write_file(request.file_path, request.content)
        elif request.operation == "delete":
            result = components["file_ops"].delete_file(request.file_path)
        elif request.operation == "list":
            result = components["file_ops"].list_directory(request.file_path)
        else:
            raise HTTPException(status_code=400, detail="Invalid operation")
        
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# System information endpoints
@app.get("/api/system/info")
async def get_system_info(api_key: str = Depends(verify_api_key)):
    """Get system information"""
    
    try:
        system_info = components["system_info"].get_system_info()
        
        return {
            "platform": system_info.platform,
            "python_version": system_info.python_version,
            "working_directory": system_info.working_directory,
            "available_space": system_info.available_space,
            "memory_usage": system_info.memory_usage
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/system/stats")
async def get_system_stats(api_key: str = Depends(verify_api_key)):
    """Get system statistics"""
    
    try:
        return {
            "memory_stats": components["memory_manager"].get_memory_stats(),
            "task_queue_status": components["task_planner"].get_queue_status(),
            "safety_stats": components["safety_guard"].get_safety_stats(),
            "policy_violations": components["policy_engine"].get_violation_stats(),
            "performance_metrics": components["self_reflection"].analyze_recent_performance().total_interactions
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Self-reflection endpoints
@app.get("/api/insights/performance")
async def get_performance_insights(api_key: str = Depends(verify_api_key)):
    """Get performance insights"""
    
    try:
        metrics = components["self_reflection"].analyze_recent_performance()
        patterns = components["self_reflection"].identify_patterns()
        recommendations = components["self_reflection"].generate_improvement_recommendations()
        
        return {
            "performance_metrics": {
                "total_interactions": metrics.total_interactions,
                "successful_interactions": metrics.successful_interactions,
                "average_response_time": metrics.average_response_time,
                "average_satisfaction": metrics.average_satisfaction,
                "improvement_areas": metrics.improvement_areas
            },
            "patterns": patterns,
            "recommendations": recommendations
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )