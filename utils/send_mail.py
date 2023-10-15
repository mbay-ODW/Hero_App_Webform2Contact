import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
from smtplib import SMTP_SSL as SMTP

# Initialize a logger for the MailSending class
logger = logging.getLogger('MailSending')

def send_email(message, to_email, smtp_server, smtp_port, smtp_user, smtp_password):
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = smtp_user
    msg['To'] = to_email
    msg['Subject'] = "Failed to parse mail content from website"
    logger.debug(f'Sending mail with the following msg: {msg}')

    # Attach the message to the email
    msg.attach(MIMEText(message, 'plain'))

    # Connect to the SMTP server and send the email
    try:
        conn = SMTP(smtp_server, smtp_port)
        conn.login(smtp_user, smtp_password)
        try:
            conn.sendmail(smtp_user, to_email, msg.as_string())
        finally:
            conn.quit()
        logger.info("Email sent successfully.")
    except Exception as e:
        logger.error(f"Failed to send email: {str(e)}")