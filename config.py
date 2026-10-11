"""
Configuration for the Financial Analyst Agent
Adjust these settings to customize agent behavior
"""

# Agent Configuration
AGENT_CONFIG = {
    # Maximum number of steps allowed in a research plan
    "max_steps": 50,
    
    # Maximum iterations for verification loops
    "max_iterations": 10,
    
    # Maximum retries per step
    "max_retries_per_step": 3,
}

# Loop Detection Configuration
LOOP_DETECTION = {
    # Window size for loop detection (number of recent steps to check)
    "window_size": 10,
    
    # Threshold for detecting loops (number of repetitions)
    "threshold": 3,
}

# Cache Configuration
CACHE_CONFIG = {
    # Time-to-live for cached data in seconds (3600 = 1 hour)
    "ttl": 3600,
    
    # Enable/disable caching
    "enabled": True,
}

# Data Quality Configuration
DATA_QUALITY = {
    # Maximum age of data in days
    "max_age_days": 365,
    
    # Require data freshness checks
    "check_freshness": True,
    
    # Tolerance for balance sheet equation (as percentage)
    "balance_sheet_tolerance": 0.01,  # 1%
}

# Output Configuration
OUTPUT_CONFIG = {
    # Show detailed execution logs
    "verbose": True,
    
    # Show verification details
    "show_verification": True,
    
    # Show cache hits
    "show_cache_hits": True,
}

# Financial Data Configuration
FINANCIAL_DATA = {
    # Default period for financial statements
    "default_period": "annual",  # "annual" or "quarterly"
    
    # Default currency
    "default_currency": "USD",
}


def get_agent_config():
    """Get agent configuration"""
    return AGENT_CONFIG


def get_loop_detection_config():
    """Get loop detection configuration"""
    return LOOP_DETECTION


def get_cache_config():
    """Get cache configuration"""
    return CACHE_CONFIG


def get_data_quality_config():
    """Get data quality configuration"""
    return DATA_QUALITY


def get_output_config():
    """Get output configuration"""
    return OUTPUT_CONFIG


def get_financial_data_config():
    """Get financial data configuration"""
    return FINANCIAL_DATA


if __name__ == "__main__":
    import json
    
    print("Current Configuration:")
    print("\nAgent:", json.dumps(AGENT_CONFIG, indent=2))
    print("\nLoop Detection:", json.dumps(LOOP_DETECTION, indent=2))
    print("\nCache:", json.dumps(CACHE_CONFIG, indent=2))
    print("\nData Quality:", json.dumps(DATA_QUALITY, indent=2))
    print("\nOutput:", json.dumps(OUTPUT_CONFIG, indent=2))
    print("\nFinancial Data:", json.dumps(FINANCIAL_DATA, indent=2))
