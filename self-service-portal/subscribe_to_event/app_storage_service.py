import boto3
from subscription_data import SubscriptionData


class SelfServiceSubscriptionToEventRequest:
    def __init__(self, unit, event_name, version):
        self.unit = unit
        self.event_name = event_name
        self.version = version

    @staticmethod
    def from_subscription_data(subscription_data: SubscriptionData):
        return SelfServiceSubscriptionToEventRequest(subscription_data.unit, subscription_data.name, subscription_data.version)


class SelfServiceStorageService:
    def __init__(self, table_name):
        self.client = boto3.client('dynamodb')
        self.table_name = table_name

    def save(self, subscription_request: SelfServiceSubscriptionToEventRequest):
        return self.client.put_item(
            TableName=self.table_name,
            Item={
                'PK': {'S': subscription_request.unit},
                'SK': {'S': f'SUBSCRIPTION#{subscription_request.event_name}#VERSION#{subscription_request.version}'},
                'Unit': {'S': subscription_request.unit},
                'EventName': {'S': subscription_request.event_name},
                'Version': {'S': f'{subscription_request.version}'},
            }
        )
