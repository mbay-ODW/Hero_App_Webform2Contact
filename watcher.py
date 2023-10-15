import os
import sys
import time
import pyfiglet

import logging
from logging.handlers import RotatingFileHandler
import pathlib

from utils.hero_graphql import HeroGraphQLConnection
from utils.get_mails import fetch_and_process_emails
from utils.send_mail import send_email


# Configure the logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Create a directory for log files
path = pathlib.Path('./')
path.mkdir(parents=True, exist_ok=True)

# Determine the logging level based on the environment variable
if os.environ.get('LOGGING_LEVEL'):
    LOGGING_LEVEL = os.environ.get('LOGGING_LEVEL')
    if os.environ.get('LOGGING_LEVEL') == 'Info':
        LOGGING_LEVEL = logging.INFO
    elif os.environ.get('LOGGING_LEVEL') == 'Error':
        LOGGING_LEVEL = logging.ERROR
    elif os.environ.get('LOGGING_LEVEL') == 'Debug':
        LOGGING_LEVEL = logging.DEBUG
    elif os.environ.get('LOGGING_LEVEL') == 'Warning':
        LOGGING_LEVEL = logging.WARNING
    else:
        LOGGING_LEVEL = logging.INFO
else:
    LOGGING_LEVEL = logging.INFO

# Set the logger's level
logger.setLevel(LOGGING_LEVEL)

# Define log formatters for console and file output
log_file_formatter = logging.Formatter('%(asctime)s %(threadName)s %(levelname)s %(name)s %(message)s')
log_console_formatter = logging.Formatter('%(asctime)s %(threadName)s %(levelname)s %(name)s %(message)s')

# Set default log format for the console
if len(logger.handlers) == 0:
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_console_formatter)
    console_handler.setLevel(LOGGING_LEVEL)
    logger.addHandler(console_handler)
else:
    handler = logger.handlers[0]
    handler.setFormatter(log_console_formatter)

# Configure rotating log files with a maximum of 5 files, each up to 10 MB
rotate_handler = RotatingFileHandler(filename=path / 'watcher.log', maxBytes=10000000, backupCount=5)
rotate_handler.setFormatter(log_file_formatter)
rotate_handler.setLevel(LOGGING_LEVEL)
logger.addHandler(rotate_handler)

# Create ASCII art with a specific font
font = pyfiglet.Figlet(font='standard', width=120)
ascii_art = font.renderText("Hero App \n Automatic contact creation \n Murat Bayram \n 15.10.2023")
# Print the ASCII art
print(ascii_art)

# Initialize the logger with a debug message
logger.debug("Starting setting Environments")

# Set environment variables and their default values
try:
    # Checking interval
    logger.debug("Setting checking interval")
    CHECK_INTERVAL = os.environ.get('CHECK_INTERVAL')
    if CHECK_INTERVAL is not None:
        logger.debug(f"Checking interval is set to: {CHECK_INTERVAL}")
    else:
        logger.info("No CHECK_INTERVAL set, using 300")
        CHECK_INTERVAL = 300
        logger.debug(f"Checking interval is set to the default value: {CHECK_INTERVAL}")

    # Email
    logger.debug("Setting email address")
    EMAIL_USERNAME = os.environ.get('EMAIL_USERNAME')
    if EMAIL_USERNAME is not None:
        logger.debug(f"E-Mail address is set to: {EMAIL_USERNAME}")
    else:
        raise Exception("EMAIL_USERNAME environment variable is not set but required")

    # Password
    logger.debug("Setting password")
    EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD')
    if EMAIL_PASSWORD is not None:
        logger.debug("Password is set.")
    else:
        raise Exception("EMAIL_PASSWORD environment variable is not set but required")

    # Email inbox
    logger.debug("Setting email inbox")
    EMAIL_INBOX = os.environ.get('EMAIL_INBOX')
    if EMAIL_INBOX is not None:
        logger.debug(f"Email inbox is set to: {EMAIL_INBOX}")
    else:
        EMAIL_INBOX = "INBOX"
        logger.debug(f"Email inbox is set to the default value: {EMAIL_INBOX}")

    # Email Subject filter
    logger.debug("Setting email subject filter")
    EMAIL_SUBJECT_FILTER = os.environ.get('EMAIL_SUBJECT_FILTER')
    if EMAIL_SUBJECT_FILTER is not None:
        logger.debug(f"Email subject is set to: {EMAIL_SUBJECT_FILTER}")
    else:
        EMAIL_SUBJECT_FILTER = "Anfrage von"
        logger.debug(f"Email subject filter is set to the default value: {EMAIL_SUBJECT_FILTER}")

    # Email From filter
    logger.debug("Setting email from filter")
    EMAIL_FROM_FILTER = os.environ.get('EMAIL_FROM_FILTER')
    if EMAIL_FROM_FILTER is not None:
        logger.debug(f"Email subject is set to: {EMAIL_FROM_FILTER}")
    else:
        EMAIL_FROM_FILTER = EMAIL_USERNAME
        logger.debug(f"Email subject filter is set to the default value: {EMAIL_FROM_FILTER}")

    # Email Alert
    logger.debug("Setting email inbox")
    EMAIL_ALERT = os.environ.get('EMAIL_ALERT')
    if EMAIL_ALERT is not None:
        if EMAIL_ALERT in ["False", "True"]:
            if EMAIL_ALERT == "False":
                EMAIL_ALERT = False
            else:
                EMAIL_ALERT = True
            logger.debug(f"Email alert is set to: {EMAIL_ALERT}")
        else:
            raise Exception("EMAIL_ALERT environment variable is either False or True")
    else:
        EMAIL_ALERT = False
    logger.debug(f"Email Alert is set to the default value: {EMAIL_ALERT}")

    # IMAP Server
    logger.debug("Setting IMAP server")
    IMAP_SERVER = os.environ.get('IMAP_SERVER')
    if IMAP_SERVER is not None:
        logger.debug(f"IMAP Server is set to: {IMAP_SERVER}")
    else:
        raise Exception("IMAP_SERVER environment variable is not set but required")

    # IMAP Port
    logger.debug("Setting IMAP port")
    IMAP_PORT = os.environ.get('IMAP_PORT', 993)
    logger.debug(f"IMAP Port is set to: {IMAP_PORT}")

    # SMTP Server
    logger.debug("Setting SMTP server")
    SMTP_SERVER = os.environ.get('SMTP_SERVER')
    if SMTP_SERVER is not None:
        logger.debug(f"SMTP Server is set to: {SMTP_SERVER}")
    elif EMAIL_ALERT is True:
        raise Exception("SMTP_SERVER environment variable is not set but required if EMAIL_ALERT is True")
    else:
        logger.debug(f"SMTP Server is not set")

    # SMTP Port
    logger.debug("Setting SMTP port")
    SMTP_PORT = os.environ.get('SMTP_PORT', 465)
    logger.debug(f"SMTP Port is set to: {SMTP_PORT}")

    # GraphQL Server
    logger.debug("Setting GraphQL server")
    GRAPHQL_SERVER = os.environ.get('GRAPHQL_SERVER')
    if GRAPHQL_SERVER is not None:
        logger.debug(f"GraphQL Server is set to: {GRAPHQL_SERVER}")
    else:
        raise Exception("GRAPHQL_SERVER environment variable is not set but required")

    # GraphQL Bearer Token
    logger.debug("Setting GraphQL bearer token")
    GRAPHQL_BEARER_TOKEN = os.environ.get('GRAPHQL_BEARER_TOKEN')
    if GRAPHQL_BEARER_TOKEN is not None:
        logger.debug(f"GraphQL Server is set")
    else:
        logger.debug("No GraphQL Bearer Token was set")

    # Hero App Measure_id
    logger.debug("Setting Hero App Measure_id")
    HERO_MEASURE_ID = os.environ.get('HERO_MEASURE_ID')
    if HERO_MEASURE_ID is not None:
        logger.debug(f"Hero App Measure_id is set")
    else:
        logger.debug("No Hero App Measure_id was set, will use later on the first one that is queried")

except Exception as e:
    logger.error(e)
    sys.exit()

# All environments are set, starting listener
logger.info("All environments are set, starting listener")

# Start the main loop
try:
    while True:
        logger.info("Starting with check interval")
        con = HeroGraphQLConnection()
        # Read and process emails
        try:
            logger.debug("Checking for emails")
            for i in fetch_and_process_emails(EMAIL_USERNAME, EMAIL_PASSWORD, IMAP_SERVER, EMAIL_INBOX, IMAP_PORT, EMAIL_SUBJECT_FILTER, EMAIL_FROM_FILTER):
                try:
                    logger.info("Got an email, will create a project and contact")
                    logger.debug(f'Got the following email:{i}')
                    logger.debug(i['data'])
                    result = con.create_contact(i['data'])
                    if result:
                        logger.info("Successfully created contact and project")
                    else:
                        logger.error("Contact and/or project was not successfully created.")
                        raise Exception("Could not create Contact or Project")
                except Exception as e:
                    logger.error(e)
                    if EMAIL_ALERT:
                        logger.error("Sending alert email")
                        message = f'Was not able to parse an Email. Email has the following content: {i}'
                        send_email(message, EMAIL_USERNAME, SMTP_SERVER, SMTP_PORT, EMAIL_USERNAME, EMAIL_PASSWORD)
        except Exception as e:
            logger.error(e)
        logger.info("Waiting for the next check interval")
        time.sleep(int(CHECK_INTERVAL))
except Exception as e:
    logger.error(e)
    sys.exit()
