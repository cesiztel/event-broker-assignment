import json
import boto3
from event_data import EventData


class SelfServiceCreateEventRequest:
    def __init__(
        self, 
        application, 
        connection_type, 
        event_type, 
        event_description, 
        schema_properties, 
        version, 
        registry_arn
    ):
        self.application = application
        self.connection_type = connection_type
        self.event_type = event_type
        self.description = event_description
        self.schema_properties = schema_properties
        self.version = version
        self.registry_arn = registry_arn

    @staticmethod
    def from_event_data(event_data: EventData, registry_arn):
        return SelfServiceCreateEventRequest(
            event_data.application, 
            event_data.connection_type,
            event_data.event_type, 
            event_data.description,
            event_data.schema_properties, 
            1, 
            registry_arn
        )


class SelfServiceStorageService:
    def __init__(self, table_name):
        self.client = boto3.client('dynamodb')
        self.table_name = table_name

    def save(self, create_event_request: SelfServiceCreateEventRequest):
        return self.client.put_item(
            TableName=self.table_name,
            Item={
                'PK': {'S': create_event_request.application},
                'SK': {'S': f'CREATE_EVENT#{create_event_request.event_type}#VERSION#{create_event_request.version}'},
                'application': {'S': create_event_request.application},
                'connection_type': {'S': create_event_request.connection_type},
                'event_type': {'S': create_event_request.event_type},
                'description': {'S': create_event_request.description},
                'schema_properties': {'S': json.dumps(create_event_request.schema_properties)},
                'version': {'S': f'{create_event_request.version}'},
                'registry_arn': {'S': create_event_request.registry_arn},
            }
        )
