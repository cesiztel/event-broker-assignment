import aws_cdk as core
import aws_cdk.assertions as assertions

from event_broker_api.event_broker_api_stack import EventBrokerApiStack

# example tests. To run these tests, uncomment this file along with the example
# resource in event_broker_api/event_broker_api_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = EventBrokerApiStack(app, "event-broker-api")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
