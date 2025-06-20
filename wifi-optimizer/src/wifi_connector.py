
import subprocess
import time
from typing import Dict, Optional
from utils.logger import setup_logger
from utils.exceptions import ConnectionError, NetworkNotFoundError
from config.settings import Config

class WiFiConnector:
    """Manages Wi-Fi connections using Windows netsh."""
    
    def __init__(self, config: Config):
        self.config = config
        self.logger = setup_logger(__name__, config.get('log_level'))
    
    def connect_to_network(self, network: Dict[str, str]) -> bool:
        """Connect to a specific Wi-Fi network."""
        ssid = network.get('ssid')
        if not ssid:
            raise ValueError("Network SSID is required")
        
        self.logger.info(f"Attempting to connect to network: {ssid}")
        
        try:
            # Check if we're already connected to this network
            if self._is_connected_to_network(ssid):
                self.logger.info(f"Already connected to {ssid}")
                return True
            
            # Attempt connection using existing profile
            if self._connect_using_profile(ssid):
                return True
            
            self.logger.warning(f"Failed to connect to {ssid}")
            return False
            
        except Exception as e:
            raise ConnectionError(f"Failed to connect to {ssid}: {str(e)}")
    
    def _connect_using_profile(self, ssid: str) -> bool:
        """Connect using existing network profile."""
        try:
            cmd = ['netsh', 'wlan', 'connect', f'name={ssid}']
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                timeout=self.config.get('connection_timeout')
            )
            
            if result.returncode == 0:
                # Wait a moment and verify connection
                time.sleep(3)
                if self._is_connected_to_network(ssid):
                    self.logger.info(f"Successfully connected to {ssid}")
                    return True
            
            self.logger.warning(f"Connection attempt failed: {result.stderr}")
            return False
            
        except subprocess.TimeoutExpired:
            self.logger.error(f"Connection to {ssid} timed out")
            return False
        except Exception as e:
            self.logger.error(f"Connection error: {e}")
            return False
    
    def _is_connected_to_network(self, ssid: str) -> bool:
        """Check if currently connected to specific network."""
        try:
            cmd = ['netsh', 'wlan', 'show', 'interfaces']
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                lines = result.stdout.split('\n')
                for line in lines:
                    if 'SSID' in line and ssid in line:
                        # Check if this interface is connected
                        return True
            
            return False
            
        except Exception as e:
            self.logger.error(f"Error checking connection status: {e}")
            return False
    
    def get_current_connection(self) -> Optional[Dict[str, str]]:
        """Get information about current Wi-Fi connection."""
        try:
            cmd = ['netsh', 'wlan', 'show', 'interfaces']
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode != 0:
                return None
            
            return self._parse_interface_info(result.stdout)
            
        except Exception as e:
            self.logger.error(f"Error getting current connection: {e}")
            return None
    
    def _parse_interface_info(self, output: str) -> Optional[Dict[str, str]]:
        """Parse interface information from netsh output."""
        lines = output.split('\n')
        interface_info = {}
        
        for line in lines:
            line = line.strip()
            if 'Name' in line and ':' in line:
                interface_info['interface'] = line.split(':', 1)[1].strip()
            elif 'State' in line and ':' in line:
                interface_info['state'] = line.split(':', 1)[1].strip()
            elif 'SSID' in line and ':' in line:
                interface_info['ssid'] = line.split(':', 1)[1].strip()
            elif 'Signal' in line and ':' in line:
                interface_info['signal'] = line.split(':', 1)[1].strip()
        
        if interface_info.get('state') == 'connected' and interface_info.get('ssid'):
            return interface_info
        
        return None
    
    def disconnect(self) -> bool:
        """Disconnect from current Wi-Fi network."""
        try:
            cmd = ['netsh', 'wlan', 'disconnect']
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode == 0:
                self.logger.info("Successfully disconnected from Wi-Fi")
                return True
            else:
                self.logger.warning(f"Disconnect failed: {result.stderr}")
                return False
                
        except Exception as e:
            self.logger.error(f"Error disconnecting: {e}")
            return False