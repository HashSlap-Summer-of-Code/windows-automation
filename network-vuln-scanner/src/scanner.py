import nmap
import json
import logging
import psutil
import socket
from datetime import datetime
from typing import Dict, List, Optional
from config.settings import *

class NetworkScanner:
    def __init__(self):
        self.nm = nmap.PortScanner()
        self.logger = self._setup_logging()
        self.scan_results = {}
        
    def _setup_logging(self) -> logging.Logger:
        """Setup logging configuration"""
        os.makedirs(LOG_DIR, exist_ok=True)
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(f"{LOG_DIR}/scanner.log"),
                logging.StreamHandler()
            ]
        )
        return logging.getLogger(__name__)
    
    def discover_local_networks(self) -> List[str]:
        """Automatically discover local network ranges"""
        networks = []
        for interface, addrs in psutil.net_if_addrs().items():
            for addr in addrs:
                if addr.family == socket.AF_INET and not addr.address.startswith('127.'):
                    # Convert IP to network range
                    ip_parts = addr.address.split('.')
                    network = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.0/24"
                    if network not in networks:
                        networks.append(network)
        return networks
    
    def scan_network_range(self, network_range: str, ports: List[int] = None) -> Dict:
        """Scan a network range for live hosts and open ports"""
        self.logger.info(f"Starting scan of network range: {network_range}")
        
        if ports is None:
            ports = COMMON_PORTS
            
        port_string = ','.join(map(str, ports))
        
        try:
            # Host discovery scan
            self.logger.info("Performing host discovery...")
            self.nm.scan(hosts=network_range, arguments='-sn')
            live_hosts = list(self.nm.all_hosts())
            
            self.logger.info(f"Found {len(live_hosts)} live hosts")
            
            scan_results = {
                'scan_time': datetime.now().isoformat(),
                'network_range': network_range,
                'total_hosts_scanned': len(live_hosts),
                'hosts': {}
            }
            
            # Port scan on live hosts
            for host in live_hosts:
                self.logger.info(f"Scanning ports on {host}")
                host_results = self._scan_host_ports(host, port_string)
                scan_results['hosts'][host] = host_results
                
            return scan_results
            
        except Exception as e:
            self.logger.error(f"Error scanning network {network_range}: {str(e)}")
            return {}
    
    def _scan_host_ports(self, host: str, port_string: str) -> Dict:
        """Scan ports on a specific host"""
        try:
            self.nm.scan(host, port_string, arguments=SCAN_ARGUMENTS)
            
            host_info = {
                'hostname': self._get_hostname(host),
                'state': self.nm[host].state(),
                'os_info': self._extract_os_info(host),
                'ports': {},
                'vulnerabilities': []
            }
            
            # Extract port information
            for protocol in self.nm[host].all_protocols():
                ports = self.nm[host][protocol].keys()
                for port in ports:
                    port_info = self.nm[host][protocol][port]
                    host_info['ports'][f"{port}/{protocol}"] = {
                        'state': port_info['state'],
                        'service': port_info.get('name', 'unknown'),
                        'version': port_info.get('version', ''),
                        'product': port_info.get('product', ''),
                        'extrainfo': port_info.get('extrainfo', ''),
                        'risk_level': self._assess_risk_level(port, port_info)
                    }
            
            return host_info
            
        except Exception as e:
            self.logger.error(f"Error scanning host {host}: {str(e)}")
            return {'error': str(e)}
    
    def _get_hostname(self, ip: str) -> str:
        """Get hostname for IP address"""
        try:
            hostname = socket.gethostbyaddr(ip)[0]
            return hostname
        except:
            return ip
    
    def _extract_os_info(self, host: str) -> Dict:
        """Extract OS information from scan results"""
        os_info = {'os': 'Unknown', 'accuracy': 0}
        try:
            if 'osclass' in self.nm[host]:
                os_classes = self.nm[host]['osclass']
                if os_classes:
                    best_match = max(os_classes, key=lambda x: int(x.get('accuracy', 0)))
                    os_info = {
                        'os': best_match.get('osfamily', 'Unknown'),
                        'version': best_match.get('osgen', ''),
                        'accuracy': best_match.get('accuracy', 0)
                    }
        except:
            pass
        return os_info
    
    def _assess_risk_level(self, port: int, port_info: Dict) -> str:
        """Assess risk level based on port and service"""
        high_risk_ports = [21, 23, 135, 139, 445, 1433, 3389, 5432]
        medium_risk_ports = [22, 25, 53, 110, 143, 993, 995]
        
        if port in high_risk_ports:
            return "HIGH"
        elif port in medium_risk_ports:
            return "MEDIUM"
        elif port_info.get('state') == 'open':
            return "LOW"
        else:
            return "INFO"
    
    def scan_all_networks(self) -> Dict:
        """Scan all configured network ranges"""
        self.logger.info("Starting comprehensive network scan")
        
        # Combine configured and discovered networks
        all_networks = set(NETWORK_RANGES)
        discovered_networks = self.discover_local_networks()
        all_networks.update(discovered_networks)
        
        comprehensive_results = {
            'scan_metadata': {
                'start_time': datetime.now().isoformat(),
                'networks_scanned': list(all_networks),
                'total_networks': len(all_networks)
            },
            'results': {}
        }
        
        for network in all_networks:
            network_results = self.scan_network_range(network)
            if network_results:
                comprehensive_results['results'][network] = network_results
        
        comprehensive_results['scan_metadata']['end_time'] = datetime.now().isoformat()
        self.scan_results = comprehensive_results
        
        return comprehensive_results
    
    def save_results(self, filename: Optional[str] = None) -> str:
        """Save scan results to JSON file"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"scan_results_{timestamp}.json"
        
        os.makedirs(REPORT_DIR, exist_ok=True)
        filepath = os.path.join(REPORT_DIR, filename)
        
        with open(filepath, 'w') as f:
            json.dump(self.scan_results, f, indent=2)
        
        self.logger.info(f"Scan results saved to {filepath}")
        return filepath