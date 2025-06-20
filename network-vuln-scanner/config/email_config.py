import os

# SMTP Configuration
SMTP_SERVER = "smtp.gmail.com"  # Change to your SMTP server
SMTP_PORT = 587
SMTP_USE_TLS = True

# Email credentials (use environment variables for security)
EMAIL_USER = os.getenv("SCANNER_EMAIL_USER", "your-email@gmail.com")
EMAIL_PASSWORD = os.getenv("SCANNER_EMAIL_PASSWORD", "your-app-password")
EMAIL_FROM = EMAIL_USER

# Email settings
EMAIL_TIMEOUT = 30
MAX_ATTACHMENT_SIZE = 10 * 1024 * 1024  # 10MB