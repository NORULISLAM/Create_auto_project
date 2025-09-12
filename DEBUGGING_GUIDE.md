# 🐛 Agentic AI Debugging Guide

This guide provides comprehensive debugging strategies for your agentic AI system.

## 📋 Quick Start

1. **Test your setup:**

   ```bash
   python test_debug.py
   ```

2. **Run comprehensive tests:**

   ```bash
   python debug_agent.py test
   ```

3. **Test individual components:**

   ```bash
   python debug_agent.py components
   ```

4. **Interactive debugging:**
   ```bash
   python debug_agent.py interactive
   ```

## 🔧 Debugging Tools Added

### 1. Enhanced Logging (`agent/graph.py`)

- ✅ Added detailed logging to all agent functions
- ✅ State transition tracking
- ✅ Error handling with context
- ✅ Progress indicators with emojis

### 2. Debug Utilities (`debug_utils.py`)

- ✅ `AgentDebugger` class for comprehensive logging
- ✅ State transition logging
- ✅ Error logging with full context
- ✅ LLM call monitoring
- ✅ Memory usage tracking
- ✅ Debug report generation

### 3. Debug Configuration (`debug_config.py`)

- ✅ Environment-specific configurations
- ✅ Configurable debug settings
- ✅ Validation utilities
- ✅ Test prompts and settings

### 4. Debug Scripts

- ✅ `debug_agent.py` - Comprehensive testing suite
- ✅ `test_debug.py` - Setup validation
- ✅ Interactive debugging mode

## 🚨 Common Issues & Solutions

### Issue 1: GROQ API Key Missing

**Symptoms:** `GROQ_API_KEY not found`
**Solution:**

```bash
export GROQ_API_KEY="your_api_key_here"
# Or create a .env file:
echo "GROQ_API_KEY=your_api_key_here" > .env
```

### Issue 2: LLM Response Failures

**Symptoms:** `Planner did not return a valid response`
**Debug Steps:**

1. Check API key validity
2. Verify model availability
3. Check network connectivity
4. Review prompt formatting

**Debug Command:**

```bash
python debug_agent.py components
```

### Issue 3: File Operation Errors

**Symptoms:** Permission errors or path issues
**Debug Steps:**

1. Check `PROJECT_ROOT` permissions
2. Verify directory structure
3. Test file operations manually

**Debug Command:**

```python
from agent.tools import PROJECT_ROOT
print(f"Project root: {PROJECT_ROOT}")
PROJECT_ROOT.mkdir(parents=True, exist_ok=True)
```

### Issue 4: State Management Issues

**Symptoms:** Missing state keys or incorrect state flow
**Debug Steps:**

1. Enable state logging
2. Check state transitions
3. Verify agent dependencies

**Debug Command:**

```bash
python debug_agent.py test
```

### Issue 5: Memory Issues

**Symptoms:** High memory usage or crashes
**Debug Steps:**

1. Monitor memory usage
2. Check for memory leaks
3. Reduce recursion limits

**Debug Command:**

```python
from debug_utils import monitor_memory_usage
print(f"Memory: {monitor_memory_usage()} MB")
```

## 🔍 Debugging Strategies

### 1. State Flow Debugging

```python
from debug_utils import AgentDebugger

debugger = AgentDebugger()
# Log state before each agent
debugger.log_state_transition("PLANNER", state, "START")
```

### 2. LLM Call Debugging

```python
# Monitor LLM calls
debugger.log_llm_call("PLANNER", prompt, response, model)
```

### 3. Error Context Debugging

```python
try:
    result = agent.invoke(state)
except Exception as e:
    debugger.log_error("AGENT", e, {"state": state})
    raise
```

### 4. Memory Monitoring

```python
from debug_utils import monitor_memory_usage

initial_memory = monitor_memory_usage()
# ... run agent ...
final_memory = monitor_memory_usage()
print(f"Memory increase: {final_memory - initial_memory} MB")
```

## 📊 Debug Reports

Debug reports are automatically generated and saved as JSON files:

- `debug_report_YYYYMMDD_HHMMSS.json` - Complete execution report
- `error_AGENT_YYYYMMDD_HHMMSS.json` - Error-specific reports
- `agent_debug.log` - Continuous logging

### Report Structure:

```json
{
  "debug_data": [
    {
      "agent": "PLANNER",
      "step": "START",
      "state_keys": ["user_prompt"],
      "timestamp": "2024-01-01T12:00:00",
      "plan_info": {
        "name": "Todo App",
        "description": "A simple todo application",
        "techstack": "HTML, CSS, JavaScript",
        "files_count": 3
      }
    }
  ],
  "summary": {
    "total_transitions": 5,
    "agents_executed": ["PLANNER", "ARCHITECT", "CODER"]
  }
}
```

## 🎯 Performance Debugging

### 1. Execution Time Monitoring

```python
import time

start_time = time.time()
result = agent.invoke(state)
end_time = time.time()
print(f"Execution time: {end_time - start_time:.2f} seconds")
```

### 2. Step-by-Step Execution

```python
# Enable verbose logging
from langchain.globals import set_verbose, set_debug
set_debug(True)
set_verbose(True)
```

### 3. Recursion Limit Debugging

```python
# Start with low limits for testing
result = agent.invoke(state, {"recursion_limit": 10})
```

## 🛠️ Advanced Debugging

### 1. Custom Debug Decorators

```python
from debug_utils import debug_agent_execution

@debug_agent_execution
def my_agent(state):
    # Your agent logic
    pass
```

### 2. State Validation

```python
from debug_utils import validate_state

required_keys = ["user_prompt", "plan"]
if not validate_state(state, required_keys):
    raise ValueError("Invalid state")
```

### 3. File Operation Testing

```python
from debug_utils import check_file_operations

if not check_file_operations():
    print("File operations failed")
```

## 📝 Debugging Checklist

Before running your agent, verify:

- [ ] GROQ_API_KEY is set
- [ ] Python 3.11+ is installed
- [ ] All dependencies are installed (`pip install -e .`)
- [ ] Project root directory is writable
- [ ] Network connectivity is available
- [ ] Debug logging is enabled

## 🚀 Running Debug Sessions

### Quick Test:

```bash
python test_debug.py
```

### Full Debug Suite:

```bash
python debug_agent.py test
```

### Component Testing:

```bash
python debug_agent.py components
```

### Interactive Mode:

```bash
python debug_agent.py interactive
```

## 📞 Getting Help

If you encounter issues:

1. **Check the logs:** Look at `agent_debug.log` and error files
2. **Run tests:** Use `python test_debug.py` to validate setup
3. **Review state:** Check debug reports for state flow issues
4. **Monitor resources:** Use memory monitoring tools
5. **Test components:** Use `python debug_agent.py components`

## 🔄 Continuous Debugging

For ongoing development:

1. Keep debug logging enabled
2. Monitor memory usage regularly
3. Review debug reports after each session
4. Test with different prompts regularly
5. Validate file operations periodically

---

**Happy Debugging! 🐛✨**
