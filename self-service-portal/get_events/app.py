import json
import os

from app_storage_service import SelfServiceStorageService


def lambda_handler(event, context):
    table_name = os.environ['TableName']
    events = SelfServiceStorageService(table_name).all()
    
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(events)
    }
