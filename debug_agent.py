"""
Debug script for testing the agentic AI system
"""
import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

from agent.graph import agent
from debug_utils import AgentDebugger, check_file_operations, monitor_memory_usage
import traceback

def test_agent_with_debugging():
    """Test the agent with comprehensive debugging"""
    
    print("🔧 Starting Agent Debug Session")
    print("=" * 50)
    
    # Initialize debugger
    debugger = AgentDebugger()
    
    # Check system prerequisites
    print("\n📋 Checking System Prerequisites:")
    print("-" * 30)
    
    # Check environment variables
    groq_api_key = os.getenv("GROQ_API_KEY")
    if groq_api_key:
        print("✅ GROQ_API_KEY found")
    else:
        print("❌ GROQ_API_KEY not found - please set this environment variable")
        return False
    
    # Check file operations
    if check_file_operations():
        print("✅ File operations working")
    else:
        print("❌ File operations failed")
        return False
    
    # Monitor initial memory
    initial_memory = monitor_memory_usage()
    print(f"📊 Initial memory usage: {initial_memory:.2f} MB")
    
    # Test prompts
    test_prompts = [
        "Create a simple hello world HTML page",
        "Build a basic calculator in JavaScript",
        "Make a todo list app with HTML, CSS, and JavaScript"
    ]
    
    print(f"\n🧪 Testing with {len(test_prompts)} different prompts:")
    print("-" * 40)
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n🔍 Test {i}: {prompt}")
        print("-" * 20)
        
        try:
            # Log state before execution
            debugger.log_state_transition("SYSTEM", {"user_prompt": prompt}, "START")
            
            # Execute agent
            result = agent.invoke(
                {"user_prompt": prompt},
                {"recursion_limit": 50}  # Reduced for testing
            )
            
            # Log successful completion
            debugger.log_state_transition("SYSTEM", result, "COMPLETE")
            
            print(f"✅ Test {i} completed successfully")
            
            # Check memory usage
            current_memory = monitor_memory_usage()
            print(f"📊 Memory usage after test {i}: {current_memory:.2f} MB")
            
        except Exception as e:
            print(f"❌ Test {i} failed: {e}")
            debugger.log_error("SYSTEM", e, {"prompt": prompt, "test_number": i})
            
            # Print traceback for debugging
            print("\n🔍 Full traceback:")
            traceback.print_exc()
            
            # Continue with next test
            continue
    
    # Save debug report
    report_file = debugger.save_debug_report()
    print(f"\n📄 Debug report saved to: {report_file}")
    
    # Final memory check
    final_memory = monitor_memory_usage()
    print(f"📊 Final memory usage: {final_memory:.2f} MB")
    print(f"📈 Memory increase: {final_memory - initial_memory:.2f} MB")
    
    print("\n🎉 Debug session completed!")
    return True

def test_individual_agents():
    """Test individual agent components"""
    print("\n🔬 Testing Individual Agent Components:")
    print("=" * 45)
    
    from agent.graph import planner_agent, architect_agent, coder_agent
    from agent.states import Plan, TaskPlan, CoderState
    
    # Test planner
    print("\n1️⃣ Testing Planner Agent:")
    try:
        test_state = {"user_prompt": "Create a simple HTML page with a button"}
        result = planner_agent(test_state)
        print("✅ Planner agent working")
        print(f"   Generated plan: {result['plan'].name}")
    except Exception as e:
        print(f"❌ Planner agent failed: {e}")
        traceback.print_exc()
    
    # Test architect (requires plan from planner)
    print("\n2️⃣ Testing Architect Agent:")
    try:
        if 'result' in locals() and 'plan' in result:
            test_state = {"plan": result["plan"]}
            arch_result = architect_agent(test_state)
            print("✅ Architect agent working")
            print(f"   Generated {len(arch_result['task_plan'].implementation_steps)} steps")
        else:
            print("⏭️ Skipping architect test (no plan available)")
    except Exception as e:
        print(f"❌ Architect agent failed: {e}")
        traceback.print_exc()
    
    print("\n✅ Individual agent testing completed!")

def interactive_debug():
    """Interactive debugging session"""
    print("\n🎮 Interactive Debug Mode:")
    print("=" * 30)
    print("Enter prompts to test the agent interactively.")
    print("Type 'quit' to exit, 'memory' to check memory, 'help' for commands.")
    
    debugger = AgentDebugger()
    
    while True:
        try:
            user_input = input("\n🔍 Enter prompt (or command): ").strip()
            
            if user_input.lower() == 'quit':
                break
            elif user_input.lower() == 'memory':
                memory = monitor_memory_usage()
                print(f"📊 Current memory usage: {memory:.2f} MB")
                continue
            elif user_input.lower() == 'help':
                print("\n📖 Available commands:")
                print("  quit - Exit interactive mode")
                print("  memory - Check memory usage")
                print("  help - Show this help")
                print("  Any other text - Test as agent prompt")
                continue
            elif not user_input:
                continue
            
            print(f"\n🚀 Testing prompt: {user_input}")
            
            result = agent.invoke(
                {"user_prompt": user_input},
                {"recursion_limit": 50}
            )
            
            print("✅ Execution completed successfully!")
            
        except KeyboardInterrupt:
            print("\n👋 Exiting interactive mode...")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            debugger.log_error("INTERACTIVE", e, {"prompt": user_input})

if __name__ == "__main__":
    print("🐛 Agent Debugging Tool")
    print("=" * 25)
    
    if len(sys.argv) > 1:
        mode = sys.argv[1].lower()
        
        if mode == "test":
            test_agent_with_debugging()
        elif mode == "components":
            test_individual_agents()
        elif mode == "interactive":
            interactive_debug()
        else:
            print("❌ Unknown mode. Use: test, components, or interactive")
    else:
        print("📖 Usage: python debug_agent.py [test|components|interactive]")
        print("\nModes:")
        print("  test        - Run comprehensive tests")
        print("  components  - Test individual agent components")
        print("  interactive - Interactive debugging session")
