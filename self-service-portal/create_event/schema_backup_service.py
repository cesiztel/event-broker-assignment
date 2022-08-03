import boto3
import json
from event_data import EventData

class SchemaBackupService():
    def __init__(self, storage_name):
        self.storage = boto3.resource('s3')
        self.storage_name = storage_name
    
    def store(self, event_data: EventData):
        self.storage.Object(
            self.storage_name, 
            f'{event_data.event_type}/1/{event_data.event_type}.json'
        ).put(
            Body=(bytes(json.dumps(event_data.schema_definition).encode('UTF-8')))
        )