import os
from event_data import EventData
from schema_definition import SchemaDefinition
from event_bridge_registry_service import EventBridgeRegistryService, EventBridgeRegistrySchema
from app_storage_service import SelfServiceStorageService, SelfServiceCreateEventRequest


def lambda_handler(event, context):
    event_data = EventData.from_request(event)
    event_data.attachSchemaContract(SchemaDefinition.generates(event_data))

    schema = EventBridgeRegistrySchema.from_event_data(event_data)
    registryResult = EventBridgeRegistryService().registry(schema)  # Registry schema on EventBridge registry

    createEventRequest = SelfServiceCreateEventRequest.from_event_data(event_data, registryResult['SchemaArn'])
    table_name = os.environ['TableName']
    SelfServiceStorageService(table_name).save(createEventRequest)  # Store the event on the main database

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": event_data.toJSON()
    }
