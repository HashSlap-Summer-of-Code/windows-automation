import os
from datetime import datetime

# Network scanning configuration
NETWORK_RANGES = [
    "192.168.1.0/24",      # Common home network
    "192.168.0.0/24",      # Alternative home network
    "10.0.0.0/24",         # Corporate network
]

# Common ports to scan (Top 100 most common)
COMMON_PORTS = [
    21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 993, 995, 1723, 3306, 3389, 5432, 5900, 8080
]

# Extended port scan (optional)
EXTENDED_PORTS = list(range(1, 1025))  # Scan ports 1-1024

# Scanning configuration
SCAN_TIMEOUT = 300  # 5 minutes timeout
SCAN_INTENSITY = "-T4"  # Aggressive timing
SCAN_ARGUMENTS = "-sS -sV -O"  # SYN scan, version detection, OS detection

# Report configuration
REPORT_DIR = "reports/current"
ARCHIVE_DIR = "reports/archive"
LOG_DIR = "logs"
TEMPLATE_DIR = "templates"

# Email configuration
EMAIL_ENABLED = True
EMAIL_RECIPIENTS = ["admin@yourdomain.com", "security@yourdomain.com"]
EMAIL_SUBJECT_PREFIX = "[Network Scanner]"

# Scheduling
SCAN_SCHEDULE = "weekly"  # weekly, daily, or custom
SCAN_DAY = "monday"  # For weekly scans
SCAN_TIME = "02:00"  # 2 AM

# Alerting thresholds
ALERT_ON_NEW_HOSTS = True
ALERT_ON_NEW_PORTS = True
ALERT_ON_VULNERABILITY_SCORE = 7.0  # CVSS score threshold