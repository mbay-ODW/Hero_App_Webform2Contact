import imapclient
import email
from email.header import decode_header
import json
import logging

# Initialize a logger for the Mail Class
logger = logging.getLogger("Mail Class logger")

# Function to parse the email content and extract relevant data
def parse_mail_content(body):
    try:
        data = {}
        data["source"] = "Website"
        address = {}
        
        # Clean the email body by removing line breaks and semicolons
        string = body.replace('=\r\n', '').replace(';', '')
        lines = string.split('=0A')  # Split the body into lines
        
        logger.debug(lines)

        for line in lines:
            entry = line.split(':')  # Split each line into key and value
            if entry[0] == 'first_name':
                data['first_name'] = entry[1]
            elif entry[0] == 'last_name':
                data['last_name'] = entry[1]
            elif entry[0] == 'email':
                data['email'] = entry[1]
            elif entry[0] == 'phone_mobile_formatted':
                data['phone_mobile_formatted'] = entry[1]
            elif entry[0] == 'partner_notes':
                data['partner_notes'] = entry[1]
            elif entry[0] == 'street':
                address['street'] = entry[1]
            elif entry[0] == 'city':
                address['city'] = entry[1]
            elif entry[0] == 'zipcode':
                address['zipcode'] = entry[1]
        
        data['address'] = address
        return data
    except Exception as e:
        logger.error(e)

# Function to fetch and process emails
def fetch_and_process_emails(user, password, imap_url, inbox_folder, imap_port, subject_filter, from_filter):
    try:
        email_data = []
        with imapclient.IMAPClient(imap_url, port=imap_port) as client:
            client.login(user, password)
            client.select_folder(inbox_folder)

            # Search for new unread emails with the specified subject and sender
            messages = client.search(['SUBJECT', subject_filter, 'FROM', from_filter, 'UNSEEN'])
            
            for uid, message_data in client.fetch(messages, ['RFC822']).items():
                email_message = email.message_from_bytes(message_data[b'RFC822'])
                
                # Iterate through the email parts to find the text/plain part
                for part in email_message.walk():
                    if part.get_content_type() == 'text/plain':
                        email_content = part.get_payload()
                        logger.debug(f'This is the raw email content: {email_content}')
                
                # Extract email subject and decode if necessary
                subject, encoding = decode_header(email_message['Subject'])[0]
                if encoding:
                    subject = subject.decode(encoding)
                else:
                    subject = subject
                
                # Create a JSON object and add it to the email_data list
                email_json = {"id": uid, "data": parse_mail_content(email_content)}
                email_data.append(email_json)
        
        return email_data
    except Exception as e:
        logger.error(e)
