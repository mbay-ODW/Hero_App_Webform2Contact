# Hero_Software_Webform2Contact

## Overview
Hero_Software_Webform2Contact is a Python microservice designed to create a contact and a project within the Hero Software based on the content of a webform sent via email.

If you find Hero Software interesting or you want to try it out, you can create an account via my referral link here: [Link](https://hero-software.de/signup/helden-werben-helden?coupon=CzcIpg)

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


Creates contact:

![Contacts](/pics/contact.png)
![Contacts](/pics/contact_2.png)

Create project on that contact

![Projects](/pics/project.png)



## Dependencies
- Python3
- Required Python libraries (e.g., `requests`, `json`, `logging`, `email`)
- Hero Software GraphQL API Token
- Hero Software Account (Trial works as well)
- Email service (e.g., SMTP server)
- Webform with correct body content (text/plain) structure according:
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
1. docker pull y509177/hero_software_webform2contact:latest
2. docker run y509177/hero_software_webform2contact

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


## Disclaimer

The Hero_App_Webform2Contact microservice is an independent project and is not officially affiliated with Hero Software. All rights related to the Hero Software and its associated trademarks, copyrights, and intellectual property are owned by Hero Software. 

The code and documentation provided in this project are intended for informational and educational purposes only and should not be considered an official product or service offered by Hero Software. Any use of the Hero software, including the Hero App, should be conducted in compliance with Hero Software's terms and conditions.

All rights to the Hero Software, Hero App, and any associated materials are reserved by Hero Software.

## License
Ssee the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments
- Thanks for Hero Software support creating me an Token and answering my GraphQL questions