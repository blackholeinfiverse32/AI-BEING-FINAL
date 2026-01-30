"""
AI Being Unified - Task Planner
Orchestrates complex multi-step tasks and agent workflows
"""
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
import asyncio

class TaskStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class TaskPriority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class TaskStep:
    step_id: str
    agent_name: str
    input_data: Dict[str, Any]
    dependencies: List[str]
    status: TaskStatus = TaskStatus.PENDING
    result: Any = None
    error: Optional[str] = None

@dataclass
class Task:
    task_id: str
    name: str
    description: str
    steps: List[TaskStep]
    priority: TaskPriority
    status: TaskStatus = TaskStatus.PENDING
    created_at: str = ""
    completed_at: Optional[str] = None
    result: Any = None

class TaskPlanner:
    def __init__(self, agent_manager, memory_manager):
        self.agent_manager = agent_manager
        self.memory_manager = memory_manager
        self.active_tasks = {}
        self.task_queue = []
        self.max_concurrent_tasks = 3
    
    def create_task(self, name: str, description: str, steps: List[Dict[str, Any]], priority: TaskPriority = TaskPriority.MEDIUM) -> str:
        """Create a new task with steps"""
        import uuid
        from datetime import datetime
        
        task_id = str(uuid.uuid4())
        
        task_steps = []
        for i, step_data in enumerate(steps):
            step = TaskStep(
                step_id=f"{task_id}_step_{i}",
                agent_name=step_data["agent"],
                input_data=step_data.get("input", {}),
                dependencies=step_data.get("dependencies", [])
            )
            task_steps.append(step)
        
        task = Task(
            task_id=task_id,
            name=name,
            description=description,
            steps=task_steps,
            priority=priority,
            created_at=datetime.now().isoformat()
        )
        
        self.task_queue.append(task)
        self.task_queue.sort(key=lambda t: t.priority.value, reverse=True)
        
        return task_id
    
    async def execute_task(self, task_id: str) -> Task:
        """Execute a specific task"""
        task = next((t for t in self.task_queue if t.task_id == task_id), None)
        if not task:
            raise ValueError(f"Task {task_id} not found")
        
        if task.status != TaskStatus.PENDING:
            return task
        
        task.status = TaskStatus.RUNNING
        self.active_tasks[task_id] = task
        
        try:
            # Execute steps based on dependencies
            completed_steps = set()
            step_results = {}
            
            while len(completed_steps) < len(task.steps):
                # Find steps that can be executed (dependencies met)
                ready_steps = [
                    step for step in task.steps
                    if step.status == TaskStatus.PENDING and
                    all(dep in completed_steps for dep in step.dependencies)
                ]
                
                if not ready_steps:
                    # Check for circular dependencies or other issues
                    pending_steps = [s for s in task.steps if s.status == TaskStatus.PENDING]
                    if pending_steps:
                        raise RuntimeError("Circular dependency or unresolvable dependencies detected")
                    break
                
                # Execute ready steps
                for step in ready_steps:
                    step.status = TaskStatus.RUNNING
                    
                    try:
                        # Prepare input data with results from previous steps
                        input_data = step.input_data.copy()
                        for dep in step.dependencies:
                            if dep in step_results:
                                input_data[f"dep_{dep}"] = step_results[dep]
                        
                        # Execute the step
                        result = await self.agent_manager.execute_agent(step.agent_name, input_data)
                        
                        step.result = result
                        step.status = TaskStatus.COMPLETED
                        step_results[step.step_id] = result.result
                        completed_steps.add(step.step_id)
                        
                    except Exception as e:
                        step.error = str(e)
                        step.status = TaskStatus.FAILED
                        raise RuntimeError(f"Step {step.step_id} failed: {e}")
            
            # Task completed successfully
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.now().isoformat()
            task.result = {
                "steps": [{"step_id": s.step_id, "result": s.result} for s in task.steps],
                "final_result": step_results.get(task.steps[-1].step_id) if task.steps else None
            }
            
        except Exception as e:
            task.status = TaskStatus.FAILED
            task.result = {"error": str(e)}
        
        finally:
            if task_id in self.active_tasks:
                del self.active_tasks[task_id]
        
        return task
    
    async def execute_next_task(self) -> Optional[Task]:
        """Execute the next highest priority task"""
        if not self.task_queue or len(self.active_tasks) >= self.max_concurrent_tasks:
            return None
        
        # Find next pending task
        next_task = next((t for t in self.task_queue if t.status == TaskStatus.PENDING), None)
        if not next_task:
            return None
        
        return await self.execute_task(next_task.task_id)
    
    def get_task_status(self, task_id: str) -> Optional[Task]:
        """Get status of a specific task"""
        # Check active tasks first
        if task_id in self.active_tasks:
            return self.active_tasks[task_id]
        
        # Check task queue
        return next((t for t in self.task_queue if t.task_id == task_id), None)
    
    def cancel_task(self, task_id: str) -> bool:
        """Cancel a pending task"""
        task = self.get_task_status(task_id)
        if task and task.status == TaskStatus.PENDING:
            task.status = TaskStatus.CANCELLED
            return True
        return False
    
    def get_queue_status(self) -> Dict[str, Any]:
        """Get overall queue status"""
        status_counts = {}
        for status in TaskStatus:
            status_counts[status.value] = len([t for t in self.task_queue if t.status == status])
        
        return {
            "total_tasks": len(self.task_queue),
            "active_tasks": len(self.active_tasks),
            "status_breakdown": status_counts,
            "queue_length": len([t for t in self.task_queue if t.status == TaskStatus.PENDING])
        }
    
    def create_simple_task(self, agent_name: str, input_data: Dict[str, Any], name: str = "Simple Task") -> str:
        """Create a simple single-step task"""
        steps = [{
            "agent": agent_name,
            "input": input_data,
            "dependencies": []
        }]
        return self.create_task(name, f"Execute {agent_name}", steps)
    
    def create_workflow_task(self, workflow_steps: List[str], input_data: Dict[str, Any], name: str = "Workflow Task") -> str:
        """Create a sequential workflow task"""
        steps = []
        for i, agent_name in enumerate(workflow_steps):
            step_input = input_data.copy() if i == 0 else {}
            dependencies = [f"{name.replace(' ', '_').lower()}_step_{i-1}"] if i > 0 else []
            
            steps.append({
                "agent": agent_name,
                "input": step_input,
                "dependencies": dependencies
            })
        
        return self.create_task(name, f"Sequential workflow: {' -> '.join(workflow_steps)}", steps)