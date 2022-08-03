import os

from subscription_data import SubscriptionData
from app_storage_service import SelfServiceStorageService, SelfServiceSubscriptionToEventRequest
from consumer_deploy_config import ConsumerComponentsConfigStoreService


def lambda_handler(event, context):
    table_name = os.environ['TableName']
    consumer_components_bucket = os.environ['ConsumerComponentsBucketName']

    subscription_data = SubscriptionData.from_request(event)

    subscription_request = SelfServiceSubscriptionToEventRequest.from_subscription_data(subscription_data)

    # Save subscription   
    SelfServiceStorageService(table_name).save(subscription_request)  

    # Store the consumer configuration
    ConsumerComponentsConfigStoreService(consumer_components_bucket).store(subscription_data)

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": subscription_data.toJSON()
    }
