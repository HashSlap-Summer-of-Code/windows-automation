"""Main network management orchestrator."""

from typing import List, Dict, Optional
from src.wifi_scanner import WiFiScanner
from src.wifi_connector import WiFiConnector
from utils.logger import setup_logger
from utils.exceptions import WiFiOptimizerError
from config.settings import Config

class NetworkManager:
    """Main class that orchestrates Wi-Fi scanning and connection."""
    
    def __init__(self, config: Config):
        self.config = config
        self.logger = setup_logger(__name__, config.get('log_level'))
        self.scanner = WiFiScanner(config)
        self.connector = WiFiConnector(config)
    
    def optimize_wifi_connection(self) -> bool:
        """Find and connect to the strongest available Wi-Fi network."""
        try:
            self.logger.info("Starting Wi-Fi optimization...")
            
            # Get current connection info
            current_connection = self.connector.get_current_connection()
            if current_connection:
                self.logger.info(f"Currently connected to: {current_connection.get('ssid')}")
            
            # Scan for available networks
            networks = self.scanner.scan_networks()
            if not networks:
                self.logger.warning("No Wi-Fi networks found")
                return False
            
            # Filter and sort networks
            best_network = self._select_best_network(networks, current_connection)
            if not best_network:
                self.logger.info("No better network found")
                return False
            
            # Connect to the best network
            if self.connector.connect_to_network(best_network):
                self.logger.info(f"Successfully optimized connection to: {best_network['ssid']}")
                return True
            else:
                self.logger.error(f"Failed to connect to optimal network: {best_network['ssid']}")
                return False
                
        except Exception as e:
            self.logger.error(f"Wi-Fi optimization failed: {e}")
            return False
    
    def _select_best_network(self, networks: List[Dict], current_connection: Optional[Dict]) -> Optional[Dict]:
        """Select the best network based on signal strength and preferences."""
        
        # Filter networks
        valid_networks = []
        blacklisted = self.config.get('blacklisted_networks', [])
        signal_threshold = self.config.get('signal_threshold', -70)
        
        for network in networks:
            # Skip blacklisted networks
            if network['ssid'] in blacklisted:
                continue
                
            # Skip networks with weak signal
            signal_strength = network.get('signal_strength', 0)
            if signal_strength < abs(signal_threshold):  # Convert dBm to percentage comparison
                continue
                
            # Only include networks we have profiles for
            if not network.get('has_profile'):
                continue
                
            valid_networks.append(network)
        
        if not valid_networks:
            return None
        
        # Sort by preference and signal strength
        preferred_networks = self.config.get('preferred_networks', [])
        
        def network_score(network):
            score = network.get('signal_strength', 0)
            
            # Boost score for preferred networks
            if network['ssid'] in preferred_networks:
                score += 1000  # High boost for preferred
            
            return score
        
        # Sort networks by score (descending)
        valid_networks.sort(key=network_score, reverse=True)
        
        best_network = valid_networks[0]
        
        # Check if we should switch
        if current_connection:
            current_ssid = current_connection.get('ssid')
            current_signal = self._extract_signal_percentage(current_connection.get('signal', '0%'))
            
            # Only switch if the improvement is significant (>10%)
            if (current_ssid == best_network['ssid'] or 
                best_network['signal_strength'] - current_signal < 10):
                return None
        
        return best_network
    
    def _extract_signal_percentage(self, signal_str: str) -> int:
        """Extract signal percentage from string like '85%'."""
        try:
            return int(signal_str.replace('%', ''))
        except:
            return 0
    
    def get_network_status(self) -> Dict:
        """Get comprehensive network status information."""
        status = {
            'current_connection': self.connector.get_current_connection(),
            'available_networks': [],
            'timestamp': None
        }
        
        try:
            import datetime
            status['timestamp'] = datetime.datetime.now().isoformat()
            status['available_networks'] = self.scanner.scan_networks()
        except Exception as e:
            self.logger.error(f"Error getting network status: {e}")
        
        return status