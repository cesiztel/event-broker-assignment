from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_iam as iam
)
from constructs import Construct
from context import SystemContext


class EventBrokerApiStack(Stack):
    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            stack_name: str,
            **kwargs
    ) -> None:
        """Construct a new producer components stack"""
        super().__init__(scope, construct_id, stack_name=stack_name, **kwargs)
        context = SystemContext()

        event_producer_lambda = _lambda.Function(
            self,
            "eventProducerLambda",
            runtime=_lambda.Runtime.PYTHON_3_8,
            handler="event_producer_lambda.lambda_handler",
            code=_lambda.Code.from_asset("lambda"),
            environment={
                "EVENT_BUS_NAME": f'{context.environment}.custom.events.bus'
            },
        )

        event_policy = iam.PolicyStatement(effect=iam.Effect.ALLOW, resources=['*'], actions=['events:PutEvents'])

        event_producer_lambda.add_to_role_policy(event_policy)

        # defines an API Gateway REST API resource backed by our "producer_lambda" function.
        api = apigw.LambdaRestApi(
            self,
            'SampleAPI-EventBridge-Multi-Consumer',
            handler=event_producer_lambda,
            proxy=True,
            rest_api_name=f'{context.environment}-event-broker-api',
            deploy=False
        )

        # Define deployment and stage depending on environment
        dev_deployment = apigw.Deployment(self, id=f'{context.environment}_deployment', api=api)
        apigw.Stage(
            self, 
            id=f'stage_{context.environment}', 
            deployment=dev_deployment, 
            stage_name=context.environment
        )
