import aws_cdk as core
import aws_cdk.assertions as assertions

from event_broker_main_infrastructure.event_broker_main_infrastructure_stack import EventBrokerMainInfrastructureStack

# example tests. To run these tests, uncomment this file along with the example
# resource in event_broker_main_infrastructure/event_broker_main_infrastructure_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = EventBrokerMainInfrastructureStack(app, "event-broker-main-infrastructure")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
