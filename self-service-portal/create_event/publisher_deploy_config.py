import boto3
import json
from event_data import EventData


class PublisherComponentsConfig:

    @staticmethod
    def generates(event_data: EventData):
        return {
            "application": event_data.application,
            "event_type": event_data.event_type,
            "version": 1,
            "schema": event_data.schema_definition,
            "connection_type": event_data.connection_type
        }

class PublisherComponentsConfigStoreService:
    def __init__(self, storage_name):
        self.storage = boto3.resource('s3')
        self.storage_name = storage_name
    
    def store(self, event_data: EventData):
        s3object = self.storage.Object(
            self.storage_name, 
            f'{event_data.event_type}/1/deploy.json'
        )

        deploy_config = PublisherComponentsConfig.generates(event_data)

        s3object.put(
            Body=(bytes(json.dumps(deploy_config).encode('UTF-8')))
        )
