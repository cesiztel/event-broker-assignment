import os
from event_data import EventData
from schema_definition import SchemaDefinition
from event_bridge_registry_service import EventBridgeRegistryService, EventBridgeRegistrySchema
from app_storage_service import SelfServiceStorageService, SelfServiceCreateEventRequest
from publisher_deploy_config import PublisherComponentsConfigStoreService
from schema_backup_service import SchemaBackupService

def lambda_handler(event, context):
    table_name = os.environ['TableName']
    backup_bucket_name = os.environ['BackupBucketName']
    publisher_components_bucket = os.environ['PublisherComponentsBucketName']

    event_data = EventData.from_request(event)
    event_data.attachSchemaContract(SchemaDefinition.generates(event_data))

    # Registry schema on EventBridge registry
    schema = EventBridgeRegistrySchema.from_event_data(event_data)
    registryResult = EventBridgeRegistryService().registry(schema)

    # Store the event on the main database
    createEventRequest = SelfServiceCreateEventRequest.from_event_data(event_data, registryResult['SchemaArn'])
    SelfServiceStorageService(table_name).save(createEventRequest)

    # Store the schema in the backup service
    SchemaBackupService(backup_bucket_name).store(event_data)

    # Store the producer configuration
    PublisherComponentsConfigStoreService(publisher_components_bucket).store(event_data)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": event_data.toJSON()
    }
