import smtplib
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from typing import List, Optional
from config.email_config import *
from config.settings import EMAIL_RECIPIENTS, EMAIL_SUBJECT_PREFIX

class EmailNotifier:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def send_report(self, 
                   subject: str, 
                   text_content: str, 
                   html_report_path: Optional[str] = None,
                   recipients: List[str] = None) -> bool:
        """Send email report with optional HTML attachment"""
        
        if not EMAIL_ENABLED:
            self.logger.info("Email notifications disabled")
            return True
            
        if recipients is None:
            recipients = EMAIL_RECIPIENTS
            
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['From'] = EMAIL_FROM
            msg['To'] = ', '.join(recipients)
            msg['Subject'] = f"{EMAIL_SUBJECT_PREFIX} {subject}"
            
            # Add text content
            text_part = MIMEText(text_content, 'plain')
            msg.attach(text_part)
            
            # Add HTML report as attachment if provided
            if html_report_path and os.path.exists(html_report_path):
                self._attach_file(msg, html_report_path)
            
            # Send email
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                if SMTP_USE_TLS:
                    server.starttls()
                server.login(EMAIL_USER, EMAIL_PASSWORD)
                server.send_message(msg)
            
            self.logger.info(f"Email sent successfully to {', '.join(recipients)}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send email: {str(e)}")
            return False
    
    def _attach_file(self, msg: MIMEMultipart, file_path: str):
        """Attach file to email message"""
        try:
            # Check file size
            file_size = os.path.getsize(file_path)
            if file_size > MAX_ATTACHMENT_SIZE:
                self.logger.warning(f"File {file_path} too large ({file_size} bytes), skipping attachment")
                return
            
            with open(file_path, 'rb') as attachment:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(attachment.read())
            
            encoders.encode_base64(part)
            part.add_header(
                'Content-Disposition',
                f'attachment; filename= {os.path.basename(file_path)}'
            )
            msg.attach(part)
            
        except Exception as e:
            self.logger.error(f"Failed to attach file {file_path}: {str(e)}")
    
    def send_alert(self, alert_type: str, message: str, urgent: bool = False):
        """Send security alert email"""
        subject = f"{'URGENT - ' if urgent else ''}Security Alert: {alert_type}"
        
        alert_content = f"""
NETWORK SECURITY ALERT
======================

Alert Type: {alert_type}
Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Urgency: {'HIGH' if urgent else 'NORMAL'}

Details:
{message}

Please review your network security immediately.
        """
        
        return self.send_report(subject, alert_content)