"""Main application entry point for Wi-Fi optimizer."""

import sys
import argparse
import json
from pathlib import Path
from config.settings import Config
from src.network_manager import NetworkManager
from utils.logger import setup_logger

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description='Wi-Fi Network Optimizer')
    parser.add_argument('--config', type=str, help='Configuration file path')
    parser.add_argument('--scan-only', action='store_true', help='Only scan networks, do not connect')
    parser.add_argument('--status', action='store_true', help='Show current network status')
    parser.add_argument('--optimize', action='store_true', help='Optimize Wi-Fi connection')
    parser.add_argument('--verbose', action='store_true', help='Enable verbose logging')
    
    args = parser.parse_args()
    
    # Load configuration
    config = Config(args.config)
    
    if args.verbose:
        config.set('log_level', 'DEBUG')
    
    logger = setup_logger(__name__, config.get('log_level'))
    
    try:
        # Initialize network manager
        network_manager = NetworkManager(config)
        
        if args.status:
            # Show network status
            status = network_manager.get_network_status()
            print(json.dumps(status, indent=2))
            
        elif args.scan_only:
            # Scan networks only
            networks = network_manager.scanner.scan_networks()
            print(f"Found {len(networks)} networks:")
            for network in networks:
                print(f"  {network['ssid']}: {network.get('signal_strength', 'N/A')}% signal")
                
        elif args.optimize:
            # Optimize connection
            success = network_manager.optimize_wifi_connection()
            if success:
                print("Wi-Fi connection optimized successfully!")
                sys.exit(0)
            else:
                print("Failed to optimize Wi-Fi connection.")
                sys.exit(1)
        else:
            # Default: optimize connection
            success = network_manager.optimize_wifi_connection()
            if success:
                print("Wi-Fi connection optimized successfully!")
            else:
                print("Failed to optimize Wi-Fi connection.")
                sys.exit(1)
                
    except KeyboardInterrupt:
        logger.info("Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Application error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()