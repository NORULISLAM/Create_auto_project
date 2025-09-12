"""
Debugging utilities for the agentic AI system
"""
import json
import traceback
from typing import Dict, Any
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('agent_debug.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

class AgentDebugger:
    """Debugging utilities for agent execution"""
    
    def __init__(self, log_file: str = "agent_debug.log"):
        self.log_file = log_file
        self.debug_data = []
    
    def log_state_transition(self, agent_name: str, state: Dict[str, Any], step: str = ""):
        """Log state transitions between agents"""
        debug_info = {
            "agent": agent_name,
            "step": step,
            "state_keys": list(state.keys()),
            "timestamp": str(pd.Timestamp.now())
        }
        
        # Log specific state information
        if "plan" in state:
            plan = state["plan"]
            debug_info["plan_info"] = {
                "name": plan.name,
                "description": plan.description,
                "techstack": plan.techstack,
                "files_count": len(plan.files)
            }
        
        if "task_plan" in state:
            task_plan = state["task_plan"]
            debug_info["task_plan_info"] = {
                "steps_count": len(task_plan.implementation_steps),
                "current_step": getattr(task_plan, 'current_step_idx', 'N/A')
            }
        
        if "coder_state" in state:
            coder_state = state["coder_state"]
            debug_info["coder_state_info"] = {
                "current_step_idx": coder_state.current_step_idx,
                "total_steps": len(coder_state.task_plan.implementation_steps)
            }
        
        self.debug_data.append(debug_info)
        logger.info(f"State transition: {agent_name} - {step}")
        logger.debug(f"State data: {json.dumps(debug_info, indent=2)}")
    
    def log_error(self, agent_name: str, error: Exception, context: Dict[str, Any] = None):
        """Log errors with full context"""
        error_info = {
            "agent": agent_name,
            "error_type": type(error).__name__,
            "error_message": str(error),
            "traceback": traceback.format_exc(),
            "context": context or {},
            "timestamp": str(pd.Timestamp.now())
        }
        
        logger.error(f"Error in {agent_name}: {error}")
        logger.debug(f"Error details: {json.dumps(error_info, indent=2)}")
        
        # Save to file for later analysis
        with open(f"error_{agent_name}_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.json", "w") as f:
            json.dump(error_info, f, indent=2)
    
    def log_llm_call(self, agent_name: str, prompt: str, response: Any, model: str = "unknown"):
        """Log LLM calls for debugging"""
        llm_info = {
            "agent": agent_name,
            "model": model,
            "prompt_length": len(prompt),
            "response_type": type(response).__name__,
            "timestamp": str(pd.Timestamp.now())
        }
        
        logger.debug(f"LLM call in {agent_name}: {model}")
        logger.debug(f"Prompt length: {len(prompt)} chars")
        logger.debug(f"Response type: {type(response).__name__}")
    
    def save_debug_report(self, filename: str = None):
        """Save complete debug report"""
        if not filename:
            filename = f"debug_report_{pd.Timestamp.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        report = {
            "debug_data": self.debug_data,
            "summary": {
                "total_transitions": len(self.debug_data),
                "agents_executed": list(set(d["agent"] for d in self.debug_data))
            }
        }
        
        with open(filename, "w") as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Debug report saved to {filename}")
        return filename

def debug_agent_execution(func):
    """Decorator to add debugging to agent functions"""
    def wrapper(*args, **kwargs):
        agent_name = func.__name__.replace("_agent", "").upper()
        debugger = AgentDebugger()
        
        try:
            logger.info(f"Starting {agent_name} agent")
            result = func(*args, **kwargs)
            logger.info(f"Completed {agent_name} agent successfully")
            return result
        except Exception as e:
            debugger.log_error(agent_name, e, {"args": str(args), "kwargs": str(kwargs)})
            raise
    
    return wrapper

def validate_state(state: Dict[str, Any], required_keys: list) -> bool:
    """Validate that state contains required keys"""
    missing_keys = [key for key in required_keys if key not in state]
    if missing_keys:
        logger.error(f"Missing required state keys: {missing_keys}")
        return False
    return True

def check_file_operations():
    """Check if file operations are working correctly"""
    from agent.tools import PROJECT_ROOT
    
    try:
        # Test project root creation
        PROJECT_ROOT.mkdir(parents=True, exist_ok=True)
        logger.info(f"Project root created/verified: {PROJECT_ROOT}")
        
        # Test file operations
        test_file = PROJECT_ROOT / "test_debug.txt"
        test_file.write_text("Debug test content")
        
        if test_file.exists():
            logger.info("File write operation successful")
            test_file.unlink()  # Clean up
            logger.info("File cleanup successful")
        else:
            logger.error("File write operation failed")
            
    except Exception as e:
        logger.error(f"File operations check failed: {e}")
        return False
    
    return True

def monitor_memory_usage():
    """Monitor memory usage during execution"""
    import psutil
    import os
    
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    
    logger.info(f"Memory usage: {memory_info.rss / 1024 / 1024:.2f} MB")
    return memory_info.rss / 1024 / 1024  # Return MB

# Import pandas for timestamp (add to dependencies if needed)
try:
    import pandas as pd
except ImportError:
    # Fallback to datetime if pandas not available
    from datetime import datetime
    class pd:
        class Timestamp:
            @staticmethod
            def now():
                return datetime.now()
