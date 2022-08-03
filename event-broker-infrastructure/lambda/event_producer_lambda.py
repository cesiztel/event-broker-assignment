import json
import os

import boto3
import datetime
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    event_bus_name = os.environ['EVENT_BUS_NAME']

    client = boto3.client('events')
    event_path: str = event["pathParameters"]["proxy"]
    event_body = json.loads(event["body"])

    # Structure of EventBridge Event
    eb_event = {
        'Time': datetime.datetime.now(),
        'Source': event_body["metadata"]["event_attributes"]["source"],
        'Detail': json.dumps(event_body),
        'DetailType': f'{event_path.replace("/", ".")}',
        'EventBusName': event_bus_name,
    }
    logger.info(eb_event)

    # Send event to EventBridge
    response = client.put_events(
        Entries=[
            eb_event
        ]
    )

    logger.info(response)

    # Returns success reponse to API Gateway
    return {
        "statusCode": 200,
        "body": json.dumps({
            "result": "from Producer"
        }),
    }