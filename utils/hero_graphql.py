import requests
import json
import logging
import os
from graphql_query import Argument, Operation, Query

# Initialize a logger for the HeroGraphQLConnection class
logger = logging.getLogger('Hero GraphQL Connection Class')

class HeroGraphQLConnection():
    def __init__(self):
        try:
            self.logger = logging.getLogger('Hero GraphQL Connection Class')
            self.url = os.environ.get('GRAPHQL_SERVER')
            self.token = os.environ.get('GRAPHQL_BEARER_TOKEN')
            self.headers = {}
            self.headers["Content-Type"] = "application/json"
            self.headers["Authorization"] = f"Bearer {self.token}"
            self.logger.debug("Checking connection")
            self.check_connection()
            self.logger.debug("Connection checked")
            HERO_MEASURE_ID = os.environ.get('HERO_MEASURE_ID')
            if HERO_MEASURE_ID is None:
                self.logger.debug("Hero measure id is none, requesting one.")
                self.get_mearsure_id()
            self.measure_id = os.environ.get('HERO_MEASURE_ID')
        except Exception as e:
            self.logger.error(e)

    def check_connection(self):
        try:
            payload = "{\"query\":\"query {\\n   contacts {\\n      id\\n   }\\n}\"}"
            response = requests.request("POST", self.url, data=payload, headers=self.headers)
            if response.status_code == 200:
                data = response.json()
                if 'errors' in data:
                    raise Exception(f"First GraphQL Error: {data['errors'][0]['message']}")
                self.logger.debug("Connection to GraphQL works")
            else:
                raise Exception(f"GraphQL gave status code: {response.status_code}")
        except Exception as e:
            self.logger.error(e)

    def create_contact(self, contact):
        try:
            self.logger.debug("Creating a new contact")
            self.contact = contact
            self.logger.debug(f'Received the following contact details: {self.contact}')
            self.notes = {self.contact['partner_notes']}
            self.logger.debug(f'Extracted the following notes: {self.notes}')
            payload = self.create_graphql_mutation_contact(self.contact)
            data = {}
            data['query'] = payload
            self.logger.debug(f'Payload for the request to GraphQL looks like: {json.dumps(data)}. Sending data to the GraphQL Server.')
            response = requests.request("POST", self.url, data=json.dumps(data), headers=self.headers)
            self.logger.debug(f'Received status code: {response.status_code} and text {response.text}')
            if response.status_code == 200:
                try:
                    # Parse the response content as JSON
                    data = response.json()
                    self.logger.debug(f'The data was in the response: {data}. Checking for errors.')
                    if 'errors' in data:
                        raise Exception(f"First GraphQL Error: {data['errors'][0]['message']}")
                    self.customer_id = data['data']['create_contact']['id']
                    self.logger.debug("No errors")
                    self.logger.info(f"Customer was created with id: {self.customer_id}")
                    self.logger.debug(f'Extracted the following customer_id: {self.customer_id}')
                    self.logger.info("Creating a project for that customer")
                    return self.create_project()
                except Exception as e:
                    self.logger.error(e)
            else:
                raise Exception(f"The following status code was given: {response.status_code} with the following error: {response.text}")
        except Exception as e:
            self.logger.error(e)

    def create_project(self):
        try:
            payload = self.create_graphql_mutation_project(self.contact)
            data = {}
            data['query'] = payload
            self.logger.debug(f'Payload for the request to GraphQL for a project looks like: {json.dumps(data)}. Sending data to the GraphQL Server.')
            response = requests.request("POST", self.url, data=json.dumps(data), headers=self.headers)
            self.logger.debug(f'Received status code: {response.status_code} and text {response.text}')
            if response.status_code == 200:
                try:
                    # Parse the response content as JSON
                    data = response.json()
                    self.logger.debug(f'The data was in the response: {data}. Checking for errors.')
                    if 'errors' in data:
                        raise Exception(f"First GraphQL Error: {data['errors'][0]['message']}")
                    self.logger.debug("No errors")
                    self.logger.info("Project was created")
                    return data
                except Exception as e:
                    self.logger.error(e)
            else:
                raise Exception
        except Exception as e:
            self.logger.error(e)

    def check_contact_exists(self):
        try:
            pass
        except:
            pass

    def create_graphql_mutation_contact(self, contact_data):
        try:
            # Construct the mutation payload dictionary
            self.logger.debug(f'Creating a GraphQL query string based on the following data: {contact_data}')
            street = Argument(name="street", value=f'"{contact_data["address"]["street"]}"')
            city = Argument(name="street", value=f'"{contact_data["address"]["city"]}"')
            zipcode = Argument(name="zipcode", value=f'"{contact_data["address"]["zipcode"]}"')
            address = Argument(name="address", value=[street, city, zipcode])
            source = Argument(name="source", value='"Website"')
            phone = Argument(name="phone_mobile_formatted", value=f'"{contact_data["phone_mobile_formatted"]}"')
            email = Argument(name="email", value=f'"{contact_data["email"]}"')
            first_name = Argument(name="first_name", value=f'"{contact_data["first_name"]}"')
            last_name = Argument(name="last_name", value=f'"{contact_data["last_name"]}"')
            contact = Argument(name="contact", value=[first_name, last_name, email, phone, source, address])
            mutation_payload = Operation(type="mutation create_contact", queries=[Query(name="create_contact", arguments=[contact], fields=['id'])])
            self.logger.debug(f'Created the following GraphQL query: {mutation_payload.render()}')
            return mutation_payload.render()
        except Exception as e:
            self.logger.error(e)

    def get_mearsure_id(self):
        try:
            self.logger.debug("Getting measure_id")
            payload = "{\"query\":\"query { \\n   project_matches(first: 1){\\n      measure_id\\n   } \\n}\"}"
            response = requests.request("POST", self.url, data=payload, headers=self.headers)
            data = response.json()
            if 'errors' in data:
                raise Exception(f"First GraphQL Error: {data['errors'][0]['message']}")
            else:
                matches = data['data']['project_matches']
                self.measure_id = matches[0]['measure_id']
            os.environ.setdefault('HERO_MEASURE_ID', str(self.measure_id))
            self.logger.info(f"HERO_MEASURE_ID was set to {self.measure_id}")
        except Exception as e:
            self.logger.error(e)

    def create_graphql_mutation_project(self, project_data):
        try:
            self.logger.debug(f'Creating a GraphQL query string based on the following data: {project_data}')
            street = Argument(name="street", value=f'"{project_data["address"]["street"]}"')
            city = Argument(name="city", value=f'"{project_data["address"]["city"]}"')
            zipcode = Argument(name="zipcode", value=f'"{project_data["address"]["zipcode"]}"')
            address = Argument(name="address", value=[street, city, zipcode])
            customer_id = Argument(name="customer_id", value=f'{self.customer_id}')
            measure_id = Argument(name="measure_id", value=f'{self.measure_id}')
            project = Argument(name="project", value=[address, measure_id, customer_id])
            partner_notes = Argument(name="partner_notes", value=f'"{self.notes}"')
            project_match = Argument(name="project_match", value=[partner_notes, project])
            
            # Construct the mutation payload dictionary
            mutation_payload = Operation(type="mutation create_project", queries=[Query(name="create_project_match", arguments=[project_match], fields=['id'])])
            self.logger.debug(f'Created the following GraphQL query: {mutation_payload.render()}')
            return mutation_payload.render()
        except Exception as e:
            self.logger.error(e)