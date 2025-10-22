import unittest
from unittest.mock import Mock, patch
from src.network_manager import NetworkManager
from config.settings import Config

class TestNetworkManager(unittest.TestCase):
    
    def setUp(self):
        self.config = Config()
        self.manager = NetworkManager(self.config)
    
    @patch('src.wifi_scanner.WiFiScanner.scan_networks')
    def test_scan_networks(self, mock_scan):
        mock_scan.return_value = [
            {'ssid': 'TestNetwork', 'signal_strength': 80, 'has_profile': True}
        ]
        
        networks = self.manager.scanner.scan_networks()
        self.assertEqual(len(networks), 1)
        self.assertEqual(networks[0]['ssid'], 'TestNetwork')
    
    def test_network_selection(self):
        networks = [
            {'ssid': 'Weak', 'signal_strength': 30, 'has_profile': True},
            {'ssid': 'Strong', 'signal_strength': 80, 'has_profile': True},
            {'ssid': 'Medium', 'signal_strength': 60, 'has_profile': True}
        ]
        
        best = self.manager._select_best_network(networks, None)
        self.assertEqual(best['ssid'], 'Strong')

if __name__ == '__main__':
    unittest.main()