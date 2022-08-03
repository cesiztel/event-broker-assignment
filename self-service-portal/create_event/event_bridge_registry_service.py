import json
import boto3
from event_data import EventData


class EventBridgeRegistrySchema:
    """Instantiate a registry class data"""
    def __init__(self, content, registry_name, schema_name, contract_type):
        self.content = content
        self.registry_name = registry_name
        self.schema_name = schema_name
        self.type = contract_type

    @staticmethod
    def from_event_data(event_data: EventData):
        return EventBridgeRegistrySchema(
            json.dumps(event_data.schema_definition), 
            "self.service.portal.registry",
            event_data.event_type, 
            'JSONSchemaDraft4'
        )

class EventBridgeRegistryService:
    """Main instance that manage operations agains the registry"""
    def __init__(self):
        self.client = boto3.client('schemas')

    def registry(self, schema):
        return self.client.create_schema(
            Content=schema.content,
            RegistryName=schema.registry_name,
            SchemaName=schema.schema_name,
            Type=schema.type
        )

