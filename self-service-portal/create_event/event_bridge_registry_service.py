import json
import boto3
from event_data import EventData


class EventBridgeRegistrySchema:
    def __init__(self, content, registry_name, schema_name, contract_type):
        self.content = content
        self.registry_name = registry_name
        self.schema_name = schema_name
        self.type = contract_type

    @staticmethod
    def from_event_data(event_data: EventData):
        return EventBridgeRegistrySchema(json.dumps(event_data.schema_definition), f'{event_data.unit}.events',
                                         event_data.name, 'JSONSchemaDraft4')


class EventBridgeRegistryService:
    def __init__(self):
        self.client = boto3.client('schemas')

    def registry(self, schema: EventBridgeRegistrySchema):
        return self.client.create_schema(
            Content=schema.content,
            RegistryName=schema.registry_name,
            SchemaName=schema.schema_name,
            Type=schema.type
        )

