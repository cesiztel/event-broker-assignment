import os

from subscription_data import SubscriptionData
from app_storage_service import SelfServiceStorageService, SelfServiceSubscriptionToEventRequest


def lambda_handler(event, context):
    subscription_data = SubscriptionData.from_request(event)

    subscription_request = SelfServiceSubscriptionToEventRequest.from_subscription_data(subscription_data)
    table_name = os.environ['TableName']
    SelfServiceStorageService(table_name).save(subscription_request)  # Store subscription

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": subscription_data.toJSON()
    }
