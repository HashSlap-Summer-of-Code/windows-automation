"""Configuration settings for Wi-Fi optimizer."""

import os
from typing import List, Dict, Any

# Default configuration
DEFAULT_CONFIG = {
    'scan_timeout': 30,
    'connection_timeout': 15,
    'retry_attempts': 3,
    'signal_threshold': -70,  # dBm
    'preferred_networks': [],
    'blacklisted_networks': [],
    'log_level': 'INFO'
}

class Config:
    """Configuration manager for Wi-Fi optimizer."""
    
    def __init__(self, config_file: str = None):
        self.config = DEFAULT_CONFIG.copy()
        if config_file and os.path.exists(config_file):
            self.load_from_file(config_file)
    
    def load_from_file(self, config_file: str):
        """Load configuration from JSON file."""
        import json
        try:
            with open(config_file, 'r') as f:
                user_config = json.load(f)
                self.config.update(user_config)
        except Exception as e:
            print(f"Error loading config: {e}")
    
    def get(self, key: str, default=None):
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any):
        self.config[key] = value