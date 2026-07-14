from flask import current_app
import logging

def send_email(to, subject, body):
    # Production: integrate Flask-Mail or external transactional provider (SendGrid, SES)
    current_app.logger.info("Email sent to %s subject=%s", to, subject)
    # For now just log
    return True