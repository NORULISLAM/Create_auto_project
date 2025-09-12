"""
Simple test script to verify debugging setup
"""
import os
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent))

def test_imports():
    """Test that all modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        from agent.graph import agent
        print("✅ agent.graph imported successfully")
    except Exception as e:
        print(f"❌ Failed to import agent.graph: {e}")
        return False
    
    try:
        from agent.states import Plan, TaskPlan, CoderState
        print("✅ agent.states imported successfully")
    except Exception as e:
        print(f"❌ Failed to import agent.states: {e}")
        return False
    
    try:
        from agent.tools import write_file, read_file, PROJECT_ROOT
        print("✅ agent.tools imported successfully")
    except Exception as e:
        print(f"❌ Failed to import agent.tools: {e}")
        return False
    
    try:
        from debug_utils import AgentDebugger
        print("✅ debug_utils imported successfully")
    except Exception as e:
        print(f"❌ Failed to import debug_utils: {e}")
        return False
    
    try:
        from debug_config import DebugConfig
        print("✅ debug_config imported successfully")
    except Exception as e:
        print(f"❌ Failed to import debug_config: {e}")
        return False
    
    return True

def test_environment():
    """Test environment setup"""
    print("\n🔧 Testing environment...")
    
    # Check GROQ API key
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key:
        print("✅ GROQ_API_KEY found")
    else:
        print("❌ GROQ_API_KEY not found")
        print("   Please set GROQ_API_KEY environment variable")
        return False
    
    # Check Python version
    python_version = sys.version_info
    if python_version >= (3, 11):
        print(f"✅ Python version {python_version.major}.{python_version.minor} is compatible")
    else:
        print(f"❌ Python version {python_version.major}.{python_version.minor} is too old")
        print("   Requires Python 3.11 or higher")
        return False
    
    return True

def test_basic_functionality():
    """Test basic functionality"""
    print("\n⚙️ Testing basic functionality...")
    
    try:
        from debug_config import DebugConfig
        config = DebugConfig()
        
        if config.validate_config():
            print("✅ Configuration validation passed")
        else:
            print("❌ Configuration validation failed")
            return False
        
        # Test debugger creation
        from debug_utils import AgentDebugger
        debugger = AgentDebugger()
        print("✅ Debugger created successfully")
        
        # Test state logging
        test_state = {"test": "data", "user_prompt": "test prompt"}
        debugger.log_state_transition("TEST", test_state, "TEST_STEP")
        print("✅ State logging working")
        
        return True
        
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run all tests"""
    print("🐛 Debug Setup Test Suite")
    print("=" * 30)
    
    tests = [
        ("Import Test", test_imports),
        ("Environment Test", test_environment),
        ("Basic Functionality Test", test_basic_functionality)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running {test_name}...")
        if test_func():
            passed += 1
            print(f"✅ {test_name} PASSED")
        else:
            print(f"❌ {test_name} FAILED")
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Debug setup is ready.")
        print("\n📖 Next steps:")
        print("   1. Run: python debug_agent.py test")
        print("   2. Run: python debug_agent.py components")
        print("   3. Run: python debug_agent.py interactive")
    else:
        print("⚠️ Some tests failed. Please fix the issues before proceeding.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
