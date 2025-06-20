# Network Vulnerability Scanner

A comprehensive Python-based network security scanner that automatically scans local networks, detects open ports and services, generates detailed reports, and sends email notifications.

## Features

- **Automated Network Discovery**: Automatically discovers local network ranges
- **Port Scanning**: Scans for open ports and identifies running services
- **Risk Assessment**: Categorizes findings by risk level (HIGH, MEDIUM, LOW)
- **Scheduled Scanning**: Weekly automated scans via Task Scheduler
- **Email Notifications**: Sends detailed reports via email
- **HTML Reports**: Generates professional HTML reports
- **Historical Tracking**: Maintains scan history and archives

## Quick Start

### 1. Installation

```bash
# Clone or download the project
cd network-vuln-scanner

# Run the installation script
python scripts/install_dependencies.py