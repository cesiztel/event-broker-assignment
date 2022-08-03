import aws_cdk as core
import aws_cdk.assertions as assertions

from components_configuration_storage_service.components_configuration_storage_service_stack import ComponentsConfigurationStorageServiceStack

# example tests. To run these tests, uncomment this file along with the example
# resource in components_configuration_storage_service/components_configuration_storage_service_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = ComponentsConfigurationStorageServiceStack(app, "components-configuration-storage-service")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
