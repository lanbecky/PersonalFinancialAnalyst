"""
Personal Financial Analyst Agent
Formulates complex financial inquiries and translates them into clear, step-by-step research plans.
"""

import json
import time
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, field
from enum import Enum


class TaskStatus(Enum):
    """Status of a research task"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"
    VERIFIED = "verified"


@dataclass
class ResearchStep:
    """Represents a single step in the research plan"""
    step_id: int
    description: str
    tool_name: str
    parameters: Dict[str, Any]
    status: TaskStatus = TaskStatus.PENDING
    result: Optional[Any] = None
    verification: Optional[bool] = None
    dependencies: List[int] = field(default_factory=list)
    retry_count: int = 0
    max_retries: int = 3


@dataclass
class ResearchPlan:
    """Complete research plan for a financial query"""
    query: str
    steps: List[ResearchStep]
    created_at: float = field(default_factory=time.time)
    completed_steps: int = 0
    total_steps: int = 0


class FinancialAgent:
    """
    Main agent orchestrator that plans, executes, and verifies financial research tasks.
    
    Features:
    - Intelligent task planning
    - Autonomous execution
    - Self-verification
    - Loop detection
    - Step limits
    """
    
    def __init__(self, max_steps: int = 50, max_iterations: int = 10):
        """
        Initialize the Financial Agent
        
        Args:
            max_steps: Maximum number of steps allowed in a single plan
            max_iterations: Maximum iterations for verification loops
        """
        self.max_steps = max_steps
        self.max_iterations = max_iterations
        self.tools = {}
        self.execution_history = []
        self.loop_detector = LoopDetector()
        
    def register_tool(self, name: str, tool_func):
        """Register a tool that the agent can use"""
        self.tools[name] = tool_func
        
    def plan_research(self, query: str) -> ResearchPlan:
        """
        Break down a complex financial query into structured research steps
        
        Args:
            query: The financial question or analysis request
            
        Returns:
            ResearchPlan with ordered steps
        """
        # Use the task planner to generate steps
        from task_planner import TaskPlanner
        planner = TaskPlanner(available_tools=list(self.tools.keys()))
        steps = planner.plan(query)
        
        # Validate step count
        if len(steps) > self.max_steps:
            raise ValueError(f"Plan exceeds maximum steps ({len(steps)} > {self.max_steps})")
        
        plan = ResearchPlan(
            query=query,
            steps=steps,
            total_steps=len(steps)
        )
        
        return plan
    
    def execute_plan(self, plan: ResearchPlan) -> Dict[str, Any]:
        """
        Execute the research plan autonomously
        
        Args:
            plan: ResearchPlan to execute
            
        Returns:
            Final results dictionary
        """
        print(f"\n{'='*80}")
        print(f"EXECUTING RESEARCH PLAN")
        print(f"Query: {plan.query}")
        print(f"Total Steps: {plan.total_steps}")
        print(f"{'='*80}\n")
        
        results = {
            "query": plan.query,
            "steps_executed": [],
            "final_answer": None,
            "execution_time": 0
        }
        
        start_time = time.time()
        iteration = 0
        
        while iteration < self.max_iterations:
            iteration += 1
            all_completed = True
            
            for step in plan.steps:
                if step.status in [TaskStatus.COMPLETED, TaskStatus.VERIFIED]:
                    continue
                    
                # Check dependencies
                if not self._dependencies_met(step, plan.steps):
                    all_completed = False
                    continue
                
                # Execute step
                print(f"\n[Step {step.step_id}] {step.description}")
                print(f"Tool: {step.tool_name}")
                print(f"Parameters: {json.dumps(step.parameters, indent=2)}")
                
                try:
                    step.status = TaskStatus.IN_PROGRESS
                    
                    # Execute the tool
                    tool_func = self.tools.get(step.tool_name)
                    if not tool_func:
                        raise ValueError(f"Tool '{step.tool_name}' not found")
                    
                    step.result = tool_func(**step.parameters)
                    step.status = TaskStatus.COMPLETED
                    
                    print(f"✓ Step completed successfully")
                    
                    # Log execution
                    self.execution_history.append({
                        "step_id": step.step_id,
                        "tool": step.tool_name,
                        "timestamp": time.time()
                    })
                    
                    # Check for loops
                    if self.loop_detector.detect_loop(self.execution_history):
                        print("⚠ Loop detected! Breaking execution.")
                        break
                    
                except Exception as e:
                    print(f"✗ Step failed: {str(e)}")
                    step.retry_count += 1
                    
                    if step.retry_count >= step.max_retries:
                        step.status = TaskStatus.FAILED
                        print(f"✗ Step failed after {step.max_retries} retries")
                    else:
                        step.status = TaskStatus.PENDING
                        all_completed = False
                        
                results["steps_executed"].append({
                    "step_id": step.step_id,
                    "description": step.description,
                    "status": step.status.value,
                    "result": step.result
                })
            
            # Verify results
            if all_completed or self._should_stop(plan):
                verification_passed = self._verify_results(plan)
                
                if verification_passed:
                    print(f"\n✓ All steps verified successfully")
                    results["final_answer"] = self._synthesize_answer(plan)
                    break
                else:
                    print(f"\n⚠ Verification failed, refining results...")
                    # Refine steps that need improvement
                    self._refine_failed_steps(plan)
        
        results["execution_time"] = time.time() - start_time
        results["iterations"] = iteration
        
        print(f"\n{'='*80}")
        print(f"EXECUTION COMPLETE")
        print(f"Time: {results['execution_time']:.2f}s")
        print(f"Iterations: {iteration}")
        print(f"{'='*80}\n")
        
        return results
    
    def _dependencies_met(self, step: ResearchStep, all_steps: List[ResearchStep]) -> bool:
        """Check if all dependencies for a step are completed"""
        for dep_id in step.dependencies:
            dep_step = next((s for s in all_steps if s.step_id == dep_id), None)
            if not dep_step or dep_step.status not in [TaskStatus.COMPLETED, TaskStatus.VERIFIED]:
                return False
        return True
    
    def _should_stop(self, plan: ResearchPlan) -> bool:
        """Determine if execution should stop"""
        completed = sum(1 for s in plan.steps if s.status in [TaskStatus.COMPLETED, TaskStatus.VERIFIED])
        failed = sum(1 for s in plan.steps if s.status == TaskStatus.FAILED)
        
        # Stop if all non-failed steps are complete
        return completed + failed >= plan.total_steps
    
    def _verify_results(self, plan: ResearchPlan) -> bool:
        """
        Verify the results of the research plan
        
        Returns:
            True if verification passes, False otherwise
        """
        from verification import ResultVerifier
        verifier = ResultVerifier()
        
        for step in plan.steps:
            if step.status == TaskStatus.COMPLETED:
                is_valid = verifier.verify_step(step)
                
                if is_valid:
                    step.status = TaskStatus.VERIFIED
                    step.verification = True
                else:
                    step.verification = False
                    return False
        
        return True
    
    def _refine_failed_steps(self, plan: ResearchPlan):
        """Refine steps that failed verification"""
        for step in plan.steps:
            if step.verification is False and step.retry_count < step.max_retries:
                step.status = TaskStatus.PENDING
                step.retry_count += 1
    
    def _synthesize_answer(self, plan: ResearchPlan) -> str:
        """Synthesize final answer from all completed steps"""
        from answer_synthesizer import AnswerSynthesizer
        synthesizer = AnswerSynthesizer()
        
        return synthesizer.synthesize(plan)


class LoopDetector:
    """Detects execution loops to prevent infinite iterations"""
    
    def __init__(self, window_size: int = 10, threshold: int = 3):
        self.window_size = window_size
        self.threshold = threshold
    
    def detect_loop(self, history: List[Dict]) -> bool:
        """
        Detect if we're stuck in a loop
        
        Args:
            history: Execution history
            
        Returns:
            True if loop detected, False otherwise
        """
        if len(history) < self.window_size:
            return False
        
        # Check last N steps
        recent = history[-self.window_size:]
        
        # Count repeated step IDs
        step_counts = {}
        for entry in recent:
            step_id = entry["step_id"]
            step_counts[step_id] = step_counts.get(step_id, 0) + 1
        
        # If any step repeated too many times, we have a loop
        return any(count >= self.threshold for count in step_counts.values())


if __name__ == "__main__":
    # Example usage
    agent = FinancialAgent(max_steps=50, max_iterations=10)
    
    # Tools will be registered from financial_tools module
    print("Financial Agent initialized")
    print(f"Max steps: {agent.max_steps}")
    print(f"Max iterations: {agent.max_iterations}")
