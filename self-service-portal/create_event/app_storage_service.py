import boto3
from event_data import EventData


class SelfServiceCreateEventRequest:
    def __init__(self, unit, event_name, version, registry_arn):
        self.unit = unit
        self.event_name = event_name
        self.version = version
        self.registry_arn = registry_arn

    @staticmethod
    def from_event_data(event_data: EventData, registry_arn):
        return SelfServiceCreateEventRequest(event_data.unit, event_data.name, 0, registry_arn)


class SelfServiceStorageService:
    def __init__(self):
        self.client = boto3.client('dynamodb')

    def save(self, create_event_request: SelfServiceCreateEventRequest):
        return self.client.put_item(
            TableName='EventSchemasTable',
            Item={
                'PK': {'S': create_event_request.unit},
                'SK': {'S': f'CREATE_EVENT#{create_event_request.event_name}#VERSION#{create_event_request.version}'},
                'Unit': {'S': create_event_request.unit},
                'EventName': {'S': create_event_request.event_name},
                'Version': {'S': f'{create_event_request.version}'},
                'RegistryArn': {'S': create_event_request.registry_arn},
            }
        )
