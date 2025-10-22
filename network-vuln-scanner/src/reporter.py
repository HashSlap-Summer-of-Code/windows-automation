import json
import os
from datetime import datetime
from jinja2 import Template, FileSystemLoader, Environment
from typing import Dict, List
from config.settings import *

class ReportGenerator:
    def __init__(self):
        self.env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
        
    def generate_summary_report(self, scan_results: Dict) -> Dict:
        """Generate a summary report from scan results"""
        summary = {
            'scan_info': scan_results.get('scan_metadata', {}),
            'total_networks': 0,
            'total_hosts': 0,
            'total_open_ports': 0,
            'high_risk_findings': 0,
            'medium_risk_findings': 0,
            'new_hosts': [],
            'new_ports': [],
            'risk_breakdown': {'HIGH': 0, 'MEDIUM': 0, 'LOW': 0, 'INFO': 0},
            'top_services': {},
            'host_details': []
        }
        
        for network, network_data in scan_results.get('results', {}).items():
            summary['total_networks'] += 1
            summary['total_hosts'] += network_data.get('total_hosts_scanned', 0)
            
            for host_ip, host_data in network_data.get('hosts', {}).items():
                if 'error' in host_data:
                    continue
                    
                host_summary = {
                    'ip': host_ip,
                    'hostname': host_data.get('hostname', host_ip),
                    'os': host_data.get('os_info', {}).get('os', 'Unknown'),
                    'open_ports': [],
                    'risk_score': 0
                }
                
                for port_key, port_info in host_data.get('ports', {}).items():
                    if port_info.get('state') == 'open':
                        summary['total_open_ports'] += 1
                        
                        service = port_info.get('service', 'unknown')
                        summary['top_services'][service] = summary['top_services'].get(service, 0) + 1
                        
                        risk_level = port_info.get('risk_level', 'INFO')
                        summary['risk_breakdown'][risk_level] += 1
                        
                        if risk_level == 'HIGH':
                            summary['high_risk_findings'] += 1
                            host_summary['risk_score'] += 3
                        elif risk_level == 'MEDIUM':
                            summary['medium_risk_findings'] += 1
                            host_summary['risk_score'] += 2
                        elif risk_level == 'LOW':
                            host_summary['risk_score'] += 1
                        
                        host_summary['open_ports'].append({
                            'port': port_key,
                            'service': service,
                            'version': port_info.get('version', ''),
                            'risk_level': risk_level
                        })
                
                summary['host_details'].append(host_summary)
        
        # Sort hosts by risk score
        summary['host_details'].sort(key=lambda x: x['risk_score'], reverse=True)
        
        return summary
    
    def generate_html_report(self, scan_results: Dict, summary: Dict) -> str:
        """Generate HTML report"""
        template = self.env.get_template('report_template.html')
        
        html_content = template.render(
            scan_results=scan_results,
            summary=summary,
            generation_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        )
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_filename = f"network_scan_report_{timestamp}.html"
        report_path = os.path.join(REPORT_DIR, report_filename)
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return report_path
    
    def generate_text_summary(self, summary: Dict) -> str:
        """Generate a text summary for email"""
        text_summary = f"""
Network Security Scan Summary
=============================
Scan Date: {summary['scan_info'].get('start_time', 'Unknown')}

OVERVIEW:
- Networks Scanned: {summary['total_networks']}
- Total Hosts Found: {summary['total_hosts']}
- Total Open Ports: {summary['total_open_ports']}

RISK ASSESSMENT:
- High Risk Findings: {summary['high_risk_findings']}
- Medium Risk Findings: {summary['medium_risk_findings']}
- Low Risk Findings: {summary['risk_breakdown']['LOW']}

TOP VULNERABLE HOSTS:
"""
        
        for i, host in enumerate(summary['host_details'][:5]):  # Top 5 hosts
            text_summary += f"{i+1}. {host['hostname']} ({host['ip']}) - Risk Score: {host['risk_score']}\n"
            for port in host['open_ports'][:3]:  # Top 3 ports per host
                text_summary += f"   - {port['port']}: {port['service']} ({port['risk_level']})\n"
        
        return text_summary

# Create report template
def create_report_template():
    """Create the HTML report template"""
    template_content = """
<!DOCTYPE html>
<html>
<head>
    <title>Network Security Scan Report</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 20px; }
        .header { background-color: #2c3e50; color: white; padding: 20px; border-radius: 5px; }
        .summary { background-color: #ecf0f1; padding: 15px; margin: 20px 0; border-radius: 5px; }
        .risk-high { color: #e74c3c; font-weight: bold; }
        .risk-medium { color: #f39c12; font-weight: bold; }
        .risk-low { color: #f1c40f; }
        table { width: 100%; border-collapse: collapse; margin: 20px 0; }
        th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
        th { background-color: #34495e; color: white; }
        .host-section { margin: 20px 0; padding: 15px; border: 1px solid #bdc3c7; border-radius: 5px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>Network Security Scan Report</h1>
        <p>Generated on: {{ generation_time }}</p>
    </div>
    
    <div class="summary">
        <h2>Executive Summary</h2>
        <p><strong>Networks Scanned:</strong> {{ summary.total_networks }}</p>
        <p><strong>Total Hosts:</strong> {{ summary.total_hosts }}</p>
        <p><strong>Open Ports Found:</strong> {{ summary.total_open_ports }}</p>
        <p><strong>High Risk Findings:</strong> <span class="risk-high">{{ summary.high_risk_findings }}</span></p>
        <p><strong>Medium Risk Findings:</strong> <span class="risk-medium">{{ summary.medium_risk_findings }}</span></p>
    </div>
    
    <h2>Detailed Findings</h2>
    {% for host in summary.host_details %}
    <div class="host-section">
        <h3>{{ host.hostname }} ({{ host.ip }})</h3>
        <p><strong>OS:</strong> {{ host.os }}</p>
        <p><strong>Risk Score:</strong> {{ host.risk_score }}</p>
        
        {% if host.open_ports %}
        <table>
            <tr>
                <th>Port</th>
                <th>Service</th>
                <th>Version</th>
                <th>Risk Level</th>
            </tr>
            {% for port in host.open_ports %}
            <tr>
                <td>{{ port.port }}</td>
                <td>{{ port.service }}</td>
                <td>{{ port.version }}</td>
                <td class="risk-{{ port.risk_level.lower() }}">{{ port.risk_level }}</td>
            </tr>
            {% endfor %}
        </table>
        {% endif %}
    </div>
    {% endfor %}
</body>
</html>
"""
    
    os.makedirs(TEMPLATE_DIR, exist_ok=True)
    with open(os.path.join(TEMPLATE_DIR, 'report_template.html'), 'w') as f:
        f.write(template_content)