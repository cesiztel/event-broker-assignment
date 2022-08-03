import aws_cdk as core
import aws_cdk.assertions as assertions

from consumer_components_generator.consumer_components_generator_stack import ConsumerComponentsGeneratorStack

# example tests. To run these tests, uncomment this file along with the example
# resource in consumer_components_generator/consumer_components_generator_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ConsumerComponentsGeneratorStack(app, "consumer-components-generator")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
