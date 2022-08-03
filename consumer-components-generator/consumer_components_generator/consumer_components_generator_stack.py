import aws_cdk as cdk
from aws_cdk import (
    Stack,
    aws_events_targets as targets,
    aws_lambda as _lambda,
    aws_events as events
)
from constructs import Construct
from consumer import LambdaConsumerModel
from context import SystemContext

class LambdaConsumerConstruct(Construct):
    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            consumer: LambdaConsumerModel,
            **kwargs
    ) -> None:
        """Construct all the components for the consumer"""
        super().__init__(scope, construct_id, **kwargs)
        context = SystemContext()

        # Get the bus by name
        bus = events.EventBus.from_event_bus_name(
            scope=self,
            id='EventBusId',
            event_bus_name=f'{context.environment}.{context.event_bus_name}'
        )

        fn = _lambda.Function.from_function_attributes(
            scope=self,
            id='FunctionId',
            function_arn=consumer.arn
        )

        # Add rule
        rule = events.Rule(
            self,
            id=f"{consumer.event_type}{consumer.version}{consumer.target_unit}Rule",
            rule_name=f'{consumer.event_type}.{consumer.version}.{consumer.target_unit}.rule',
            event_pattern=events.EventPattern(
                detail={"metadata": { "event_attributes": { "target": [consumer.target_unit]} }},
                detail_type=[f'{consumer.event_type}.{consumer.version}']
            ),
            event_bus=bus
        )
        
        rule.add_target(targets.LambdaFunction(handler=fn))
        
class ConsumerComponentsGeneratorStack(Stack):
    def __init__(
        self, 
        scope: Construct, 
        construct_id: str,
        consumer: LambdaConsumerModel,
        stack_name: str,
        env: cdk.Environment,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, stack_name=stack_name, env=env, **kwargs)

        # Initialize construct. For now only LambdaConsumerModel
        if type(consumer) == LambdaConsumerModel:
            LambdaConsumerConstruct(
                scope=self,
                construct_id="ConsumerConstruct",
                consumer=consumer,
                **kwargs
            )
