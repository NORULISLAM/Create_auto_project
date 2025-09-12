"""
Debug configuration for the agentic AI system
"""
import os
from typing import Dict, Any

class DebugConfig:
    """Configuration class for debugging settings"""
    
    # Environment variables
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    DEBUG_MODE = os.getenv("DEBUG_MODE", "true").lower() == "true"
    VERBOSE_LOGGING = os.getenv("VERBOSE_LOGGING", "true").lower() == "true"
    
    # File paths
    PROJECT_ROOT = "generated_project"
    DEBUG_LOG_FILE = "agent_debug.log"
    ERROR_LOG_FILE = "agent_errors.log"
    
    # Agent settings
    DEFAULT_RECURSION_LIMIT = 100
    TEST_RECURSION_LIMIT = 50
    MAX_STEPS_PER_AGENT = 10
    
    # LLM settings
    DEFAULT_MODEL = "openai/gpt-oss-120b"
    FALLBACK_MODEL = "llama3-8b-8192"
    MAX_TOKENS = 4000
    TEMPERATURE = 0.1
    
    # Debug flags
    LOG_STATE_TRANSITIONS = True
    LOG_LLM_CALLS = True
    LOG_FILE_OPERATIONS = True
    LOG_MEMORY_USAGE = True
    SAVE_DEBUG_REPORTS = True
    
    # Test settings
    TEST_PROMPTS = [
        "Create a simple hello world HTML page",
        "Build a basic calculator in JavaScript", 
        "Make a todo list app with HTML, CSS, and JavaScript",
        "Create a responsive navigation bar",
        "Build a simple form with validation"
    ]
    
    # Error handling
    MAX_RETRIES = 3
    RETRY_DELAY = 1  # seconds
    TIMEOUT_SECONDS = 30
    
    @classmethod
    def get_llm_config(cls) -> Dict[str, Any]:
        """Get LLM configuration"""
        return {
            "model": cls.DEFAULT_MODEL,
            "max_tokens": cls.MAX_TOKENS,
            "temperature": cls.TEMPERATURE,
            "timeout": cls.TIMEOUT_SECONDS
        }
    
    @classmethod
    def get_debug_settings(cls) -> Dict[str, Any]:
        """Get debug settings"""
        return {
            "log_state_transitions": cls.LOG_STATE_TRANSITIONS,
            "log_llm_calls": cls.LOG_LLM_CALLS,
            "log_file_operations": cls.LOG_FILE_OPERATIONS,
            "log_memory_usage": cls.LOG_MEMORY_USAGE,
            "save_debug_reports": cls.SAVE_DEBUG_REPORTS,
            "debug_log_file": cls.DEBUG_LOG_FILE,
            "error_log_file": cls.ERROR_LOG_FILE
        }
    
    @classmethod
    def validate_config(cls) -> bool:
        """Validate configuration"""
        errors = []
        
        if not cls.GROQ_API_KEY:
            errors.append("GROQ_API_KEY environment variable not set")
        
        if cls.DEFAULT_RECURSION_LIMIT <= 0:
            errors.append("DEFAULT_RECURSION_LIMIT must be positive")
        
        if cls.MAX_TOKENS <= 0:
            errors.append("MAX_TOKENS must be positive")
        
        if errors:
            print("❌ Configuration errors:")
            for error in errors:
                print(f"   - {error}")
            return False
        
        print("✅ Configuration validated successfully")
        return True

# Environment-specific configurations
class DevelopmentConfig(DebugConfig):
    """Development environment configuration"""
    VERBOSE_LOGGING = True
    LOG_STATE_TRANSITIONS = True
    LOG_LLM_CALLS = True
    DEFAULT_RECURSION_LIMIT = 50

class ProductionConfig(DebugConfig):
    """Production environment configuration"""
    VERBOSE_LOGGING = False
    LOG_STATE_TRANSITIONS = False
    LOG_LLM_CALLS = False
    DEFAULT_RECURSION_LIMIT = 100

class TestingConfig(DebugConfig):
    """Testing environment configuration"""
    VERBOSE_LOGGING = True
    LOG_STATE_TRANSITIONS = True
    LOG_LLM_CALLS = True
    DEFAULT_RECURSION_LIMIT = 10
    MAX_STEPS_PER_AGENT = 3

def get_config(env: str = None) -> DebugConfig:
    """Get configuration based on environment"""
    if env is None:
        env = os.getenv("ENVIRONMENT", "development").lower()
    
    config_map = {
        "development": DevelopmentConfig,
        "production": ProductionConfig,
        "testing": TestingConfig
    }
    
    return config_map.get(env, DebugConfig)
