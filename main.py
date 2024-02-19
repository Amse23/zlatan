"""
Azure Table Storage Data Importer

This script reads customer data from a JSON file and inserts it into an Azure Table Storage.
It uses the Azure SDK for Python (azure-data-tables) to interact with the Azure Table Storage service.

Requirements:
- Install the Azure SDK for Python: pip install azure-data-tables

The script defines two TypedDict classes (Address and Customer) to represent the structure of customer data.
It also includes functions to parse the JSON file and insert entities into the Azure Table Storage.

Usage:
1. Set the 'file' variable to the path of your customer data JSON file.
2. Set the 'table_name' variable to the name of your Azure Storage Table.
3. Set the 'connection_string' variable to the connection string of Azure Storage account details.

Run the script to insert the customer data into the specified Azure Table.


"""

import json
from azure.data.tables import TableServiceClient, UpdateMode
from typing_extensions import TypedDict

# Specify the JSON file containing customer data
file = "customers.json"
# Define the name of the Azure Storage Table
table_name = 'CustomerTable'
# Define the connection string of the Azure Storage Table
connection_string = "DefaultEndpointsProtocol=https;AccountName=amsestorage;AccountKey=RuhgUHBNnfII05bbJp+XK/p1JqT0eORVT3hE/CsmtGGrGYHHM4Luns/PfCXFlJBSvIhYhdsWs/F9+AStR4YVxA==;EndpointSuffix=core.windows.net"


# Define data structures using TypedDict for better type hinting
class Address(TypedDict, total=False):
    street: str
    city: str
    state: str
    zipCode: str

class Customer(TypedDict, total=False):
    PartitionKey: str
    RowKey: str
    customerId: str
    firstName: str
    lastName: float
    email: str
    phone: str
    address: str
    dob: str
    ssn: str

# Function to parse JSON file and return data
def parse_json_file(file_address):
    """
    Parse a JSON file and return the data.

    Args:
    - file_address (str): The path to the JSON file.

    Returns:
    - list: A list of customer data dictionaries.
    """
    with open(file_address, 'r') as json_file:
        data = json.load(json_file)
        return data

# Function to insert entities into Azure Table Storage
def insert_entities(data):
    """
    Insert customer entities into Azure Table Storage.

    Args:
    - data (list): A list of customer data dictionaries.
    """
    # Connect to the Azure Storage Table using connection string
    with TableServiceClient.from_connection_string(conn_str=connection_string) as table_service_client:
        # Get the table client for the specified table
        table_client = table_service_client.get_table_client(table_name)

        # Iterate through each row in the data
        for index, row in enumerate(data):
            # Extract address information or provide default values if not present
            if row.get('address', None):
                address: Address = {
                    "street": row.get('address').get('street', ''),
                    "city": row.get('address').get('city', ''),
                    "state": row.get('address').get('state', ''),
                    "zipCode": row.get('address').get('zipCode', '')
                }
            else:
                address: Address = {
                    "street": '',
                    "city": '',
                    "state": '',
                    "zipCode": ''
                }

            # Create a Customer entity with the extracted or default values
            entity: Customer = {
                "PartitionKey": 'partition1',
                "RowKey": f'row{index}',
                "customerId": row.get('customerId', ''),
                "firstName": row.get('firstName', ''),
                "lastName": row.get('lastName', ''),
                "email": row.get('email', ''),
                "phone": row.get('phone', ''),
                "address": json.dumps(address),
                "dob": row.get('dob', ''),
                "ssn": row.get('ssn', '')
            }

            # Upsert the entity into the table (insert or update based on existence)
            table_client.upsert_entity(entity, mode=UpdateMode.REPLACE)

        # Check the inserted data by querying entities with a specified filter
        my_filter = "PartitionKey eq 'partition1'"
        entities = table_client.query_entities(my_filter)
        for entity in entities:
            print(entity)

# Entry point of the script
if __name__ == "__main__":
    # Parse the JSON file to get customer data
    parsed_data = parse_json_file(file)
    # If data is successfully parsed, insert entities into Azure Table Storage
    if parsed_data is not None:
        insert_entities(parsed_data)
