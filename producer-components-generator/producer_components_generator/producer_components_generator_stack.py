from producer import HttpsProducerModel

from aws_cdk import (
    Stack,
    aws_apigateway as apigw
)
from constructs import Construct
from context import SystemContext


class HttpsProducerConstruct(Construct):
    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            producer: HttpsProducerModel,
            **kwargs
    ) -> None:
        """Construct all the components for the producer"""
        super().__init__(scope, construct_id, **kwargs)
        context = SystemContext()

        # Get existing API resource
        rest_api = apigw.RestApi.from_rest_api_attributes(
            scope=self,
            id="RestApi",
            rest_api_id=context.apigw,
            root_resource_id=context.apigw_root_resource
        )

        # Generate model
        rest_api_model = apigw.Model(
            self,
            id="Model",
            rest_api=rest_api,
            content_type="application/json",
            schema=apigw.JsonSchema()
        )
        #
        cfn_model: apigw.CfnModel = rest_api_model.node.default_child
        cfn_model.schema = producer.schema

        # Generate the validation for that model based on JSON Schema
        request_event_validator = apigw.RequestValidator(
            self,
            id="Validator",
            rest_api=rest_api,
            request_validator_name=f"Event{producer.event_type}{producer.version}Validator",
            validate_request_parameters=False,
            validate_request_body=True
        )

        # Add the endpoint for the event and attach the model + validation
        event_resource = rest_api.root.add_resource(f"{producer.event_type}")
        event_version_resource = event_resource.add_resource(f"{producer.version}")
        event_version_resource.add_method(
            "POST",
            request_models={
                'application/json': rest_api_model
            },
            request_validator=request_event_validator
        )


class ProducerComponentsGeneratorStack(Stack):
    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            producer: HttpsProducerModel,
            stack_name: str,
            **kwargs
    ) -> None:
        """Construct a new producer components stack"""
        super().__init__(scope, construct_id, stack_name=stack_name, **kwargs)

        # Initialize construct. For now only HttpsProducerModel
        if type(producer) == HttpsProducerModel:
            HttpsProducerConstruct(
                scope=self,
                construct_id="ProducerConstruct",
                producer=producer,
                **kwargs
            )
