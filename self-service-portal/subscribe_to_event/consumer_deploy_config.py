import boto3
import json
from subscription_data import SubscriptionData


class ConsumerComponentsConfig:

    @staticmethod
    def generates(subscription_data: SubscriptionData):
        return {
            "event_type": subscription_data.event_type,
            "target_unit": subscription_data.target_unit,
            "version": subscription_data.version,
            "connection_type": subscription_data.connection_type,
            "connection_string": subscription_data.connection_string
        }

class ConsumerComponentsConfigStoreService:
    def __init__(self, storage_name):
        self.storage = boto3.resource('s3')
        self.storage_name = storage_name
    
    def store(self, subscription_data: SubscriptionData):
        s3object = self.storage.Object(
            self.storage_name, 
            f'{subscription_data.event_type}/1/deploy.json'
        )

        deploy_config = ConsumerComponentsConfig.generates(subscription_data)

        s3object.put(
            Body=(bytes(json.dumps(deploy_config).encode('UTF-8')))
        )
