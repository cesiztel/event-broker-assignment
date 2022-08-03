from aws_cdk import (
    Stack,
    aws_events as events
)
from constructs import Construct
from context import SystemContext


class EventBrokerBusStack(Stack):
    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            stack_name: str,
            **kwargs
    ) -> None:
        """Construct the main broker bus stack"""
        super().__init__(scope, construct_id, stack_name=stack_name, **kwargs)
        context = SystemContext()

        events.EventBus(
            self,
            'AuditEventBus',
            event_bus_name=f'{context.environment}.custom.events.bus'
        )
