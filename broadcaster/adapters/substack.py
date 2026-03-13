import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from .base import BaseAdapter

class SubstackAdapter(BaseAdapter):
    """
    Substack doesn't have an official API. 
    This adapter uses their Email-to-Post gateway.
    """
    def __init__(self, smtp_server="smtp.gmail.com", smtp_port=587):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.sender_email = None
        self.app_password = None

    def authenticate(self, credentials):
        """
        Expects a dict with 'email' and 'app_password'.
        (e.g., Gmail App Passwords)
        """
        self.sender_email = credentials.get("email")
        self.app_password = credentials.get("password")

    def publish(self, title, content, **kwargs):
        """
        Publishes by sending an email to your secret Substack address.
        Find this in Substack Settings > 'Drafts' or 'Email-to-post'.
        """
        target_email = kwargs.get("target_email")
        if not target_email:
            raise ValueError("Substack 'target_email' (secret address) is required.")

        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = target_email
        msg['Subject'] = title

        msg.attach(MIMEText(content, 'plain'))

        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.sender_email, self.app_password)
            server.send_message(msg)
        
        return "Email sent to Substack gateway. Check your drafts."
