"""Wi-Fi network scanner using netsh commands."""

import subprocess
import re
import json
from typing import List, Dict, Optional
from utils.logger import setup_logger
from utils.exceptions import ScanError
from config.settings import Config

class WiFiScanner:
    """Scans for available Wi-Fi networks using Windows netsh."""
    
    def __init__(self, config: Config):
        self.config = config
        self.logger = setup_logger(__name__, config.get('log_level'))
        
    def scan_networks(self) -> List[Dict[str, str]]:
        """Scan for available Wi-Fi networks."""
        try:
            self.logger.info("Starting Wi-Fi network scan...")
            
            # Execute netsh command to scan for networks
            cmd = ['netsh', 'wlan', 'show', 'profile']
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                timeout=self.config.get('scan_timeout')
            )
            
            if result.returncode != 0:
                raise ScanError(f"Failed to scan networks: {result.stderr}")
            
            profiles = self._parse_profiles(result.stdout)
            networks = []
            
            for profile in profiles:
                network_info = self._get_network_details(profile)
                if network_info:
                    networks.append(network_info)
            
            # Get current available networks
            available_networks = self._get_available_networks()
            
            # Merge profile info with available networks
            merged_networks = self._merge_network_data(networks, available_networks)
            
            self.logger.info(f"Found {len(merged_networks)} networks")
            return merged_networks
            
        except subprocess.TimeoutExpired:
            raise ScanError("Network scan timed out")
        except Exception as e:
            raise ScanError(f"Scan failed: {str(e)}")
    
    def _parse_profiles(self, output: str) -> List[str]:
        """Parse network profiles from netsh output."""
        profiles = []
        lines = output.split('\n')
        
        for line in lines:
            if 'All User Profile' in line:
                # Extract profile name using regex
                match = re.search(r':\s*(.+)$', line.strip())
                if match:
                    profiles.append(match.group(1).strip())
        
        return profiles
    
    def _get_network_details(self, profile_name: str) -> Optional[Dict[str, str]]:
        """Get detailed information about a specific network profile."""
        try:
            cmd = ['netsh', 'wlan', 'show', 'profile', f'name={profile_name}', 'key=clear']
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode != 0:
                return None
            
            return self._parse_profile_details(result.stdout, profile_name)
            
        except Exception as e:
            self.logger.warning(f"Failed to get details for {profile_name}: {e}")
            return None
    
    def _parse_profile_details(self, output: str, profile_name: str) -> Dict[str, str]:
        """Parse detailed profile information."""
        details = {
            'name': profile_name,
            'authentication': 'Unknown',
            'encryption': 'Unknown',
            'key': None
        }
        
        lines = output.split('\n')
        for line in lines:
            line = line.strip()
            if 'Authentication' in line and ':' in line:
                details['authentication'] = line.split(':', 1)[1].strip()
            elif 'Cipher' in line and ':' in line:
                details['encryption'] = line.split(':', 1)[1].strip()
            elif 'Key Content' in line and ':' in line:
                details['key'] = line.split(':', 1)[1].strip()
        
        return details
    
    def _get_available_networks(self) -> List[Dict[str, str]]:
        """Get currently available networks with signal strength."""
        try:
            cmd = ['netsh', 'wlan', 'show', 'interfaces']
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
            
            if result.returncode != 0:
                return []
            
            # Also get available networks
            cmd2 = ['netsh', 'wlan', 'show', 'networks', 'mode=bssid']
            result2 = subprocess.run(cmd2, capture_output=True, text=True, timeout=15)
            
            if result2.returncode != 0:
                return []
            
            return self._parse_available_networks(result2.stdout)
            
        except Exception as e:
            self.logger.warning(f"Failed to get available networks: {e}")
            return []
    
    def _parse_available_networks(self, output: str) -> List[Dict[str, str]]:
        """Parse available networks from netsh output."""
        networks = []
        lines = output.split('\n')
        current_network = {}
        
        for line in lines:
            line = line.strip()
            if line.startswith('SSID'):
                if current_network and current_network.get('ssid'):
                    networks.append(current_network.copy())
                current_network = {}
                ssid_match = re.search(r':\s*(.+)$', line)
                if ssid_match:
                    current_network['ssid'] = ssid_match.group(1).strip()
            elif 'Signal' in line and ':' in line:
                signal_match = re.search(r':\s*(\d+)%', line)
                if signal_match:
                    current_network['signal_strength'] = int(signal_match.group(1))
            elif 'Authentication' in line and ':' in line:
                current_network['authentication'] = line.split(':', 1)[1].strip()
            elif 'Encryption' in line and ':' in line:
                current_network['encryption'] = line.split(':', 1)[1].strip()
        
        if current_network and current_network.get('ssid'):
            networks.append(current_network)
        
        return networks
    
    def _merge_network_data(self, profiles: List[Dict], available: List[Dict]) -> List[Dict]:
        """Merge profile data with available network data."""
        merged = []
        
        for profile in profiles:
            # Find matching available network
            matching_available = None
            for avail in available:
                if avail.get('ssid') == profile.get('name'):
                    matching_available = avail
                    break
            
            if matching_available:
                # Merge data
                network = {
                    'ssid': profile['name'],
                    'signal_strength': matching_available.get('signal_strength', 0),
                    'authentication': profile.get('authentication', 'Unknown'),
                    'encryption': profile.get('encryption', 'Unknown'),
                    'available': True,
                    'has_profile': True
                }
                merged.append(network)
        
        return merged