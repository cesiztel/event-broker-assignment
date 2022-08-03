import boto3
from subscription_data import SubscriptionData


class SelfServiceSubscriptionToEventRequest:
    def __init__(self, event_type, version, target_unit, connection_type, connection_string):
        self.event_type = event_type
        self.version = version
        self.target_unit = target_unit
        self.connection_type = connection_type
        self.connection_string = connection_string

    @staticmethod
    def from_subscription_data(subscription_data: SubscriptionData):
        return SelfServiceSubscriptionToEventRequest(
            subscription_data.event_type, 
            subscription_data.version, 
            subscription_data.target_unit,
            subscription_data.connection_type,
            subscription_data.connection_string
        )


class SelfServiceStorageService:
    def __init__(self, table_name):
        self.client = boto3.client('dynamodb')
        self.table_name = table_name

    def save(self, subscription_request: SelfServiceSubscriptionToEventRequest):
        return self.client.put_item(
            TableName=self.table_name,
            Item={
                'PK': {'S': subscription_request.target_unit},
                'SK': {'S': f'SUBSCRIPTION#{subscription_request.event_type}#VERSION#{subscription_request.version}'},
                'event_type': {'S': subscription_request.event_type},
                'version': {'S': subscription_request.version},
                'target_unit': {'S': f'{subscription_request.target_unit}'},
                'connection_type': {'S': f'{subscription_request.connection_type}'},
                'connection_string': {'S': f'{subscription_request.target_unit}'}
            }
        )
