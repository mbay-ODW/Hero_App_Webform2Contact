# Hero_Software_Webform2Contact

## Overview
Hero_Software_Webform2Contact is a Python microservice designed to create a contact and a project within the Hero Software based on the content of a webform sent via email. Find more to Hero Software here on that [Link](https://hero-software.de).

Hero Software offers a GraphQL Api that can be used to automate several functionalites as well as integrate other 3rd party tools.

## Project Description
This microservice listens for incoming emails containing webform data and processes the information to create a contact and a corresponding project within the Hero Software. It serves as a bridge between webform submissions received via email and the Hero Software's data structure.

Before you can use that feature on Hero Software, you need to request an token. You can find more about that here on that [Link](https://hero-software.de/api-doku/graphql-guide).

## Features
- Receives webform data submitted via email.
- Extracts relevant information from the email content.
- Creates a new contact within the Hero Software.
- Creates a project associated with the newly created contact.
- Logs actions and errors for tracking and debugging.
- Sends email notifications for successful processing or errors.

## Dependencies
- Python3
- Required Python libraries (e.g., `requests`, `json`, `logging`, `email`)
- Hero Software GraphQL API Token
- Hero
- Email service (e.g., SMTP server)
- Webform with correct body content structure according:
    ```txt
    first_name:FIRSTNAME;
    last_name:LASTNAME;
    email:test@example.com;
    phone_mobile_formatted:+491234567890;
    street:Hauptweg 1;
    city:STADT;
    zipcode:64000;
    partner_notes:NOTES;
    ```

## Installation (Run native)
1. Clone the Hero_Software_Webform2Contact repository from [GitHub](https://github.com/your/repository).
2. Install the required Python libraries by running pip3 install -r requirements.txt
3. Load the environment files, see env.template for examples
4. Run watcher.py

## Installation (Run via docker)
1. Clone the Hero_Software_Webform2Contact repository from [GitHub](https://github.com/your/repository).
2. docker build
3. docker run -e .env

## Installation (Run via docker-compose)
1. Clone the Hero_Software_Webform2Contact repository from [GitHub](https://github.com/your/repository).
2. docker-compose up

## Installation (dockerhub)
Docker hub image will follow soon

## Components
The project consists of the following major components:

1. **Mail Listener**
   - Monitors the email inbox for incoming webform submissions. Mails that should be parsed are filtered by FROM and SUBJECT properties
   - Extracts email content
   - Calls the parsing function to convert email content into structured data.

2. **Data Parser**
   - Parses the email content and extracts key data elements, such as first name, last name, email, phone number, address, and more.
   - Prepares the data in a suitable format for creating contacts and projects following the GraphQL Api

3. **Hero GraphQL Connection**
   - Establishes a connection to the Hero Software's GraphQL server.
   - Checks the connection status and authentication.
   - Creates contacts and projects within the Hero Software using GraphQL mutations.
   - Find more about the GraphQL data model here: [Link](https://support.hero-software.de/hc/de/sections/360002779531-Schnittstellen).

4. **Email Notification**
   - Sends email notifications to specified recipients.
   - Notifies administrators of errors during data processing.

## Configuration
The following environment variables are used for configuration:

- `CHECK_INTERVAL`: The time interval for checking the email inbox.
- `EMAIL_USERNAME`: The email address used for receiving webform submissions.
- `EMAIL_PASSWORD`: The password for the email account.
- `EMAIL_INBOX`: The name of the email inbox where webform submissions are received.
- `EMAIL_SUBJECT_FILTER`: The filter to identify relevant email subjects.
- `EMAIL_FROM_FILTER`: The filter to identify relevant email senders.
- `EMAIL_ALERT`: Boolean flag to enable or disable email alerts which send an email content that could not be parsed
- `IMAP_SERVER`: The IMAP server for incoming emails.
- `IMAP_PORT`: The IMAP server port.
- `SMTP_SERVER`: The SMTP server for sending email notifications.
- `SMTP_PORT`: The SMTP server port.
- `GRAPHQL_SERVER`: The Hero Software's GraphQL server URL.
- `GRAPHQL_BEARER_TOKEN`: The bearer token for authenticating with the Hero Software.
- `HERO_MEASURE_ID`: The Hero Software measure ID used for project creation.

## Logging
The project utilizes logging to track its operation and to report any encountered errors. Log files are stored in a directory for reference.



## License
Ssee the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments
- If you find Hero Software interesting you can create an account via my referal link here: [Link](https://hero-software.de/signup/helden-werben-helden?coupon=CzcIpg)