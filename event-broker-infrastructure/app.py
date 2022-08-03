#!/usr/bin/env python3
import aws_cdk as cdk
from context import SystemContext
from event_broker_api.event_broker_api_stack import EventBrokerApiStack
from event_broker_bus.event_broker_bus import EventBrokerBusStack


def build_app() -> cdk.App:
    """Build the CDK app"""
    context = SystemContext()
    app = cdk.App()

    EventBrokerApiStack(
        app,
        "EventBrokerApiStackAppStack",
        stack_name=f'{context.environment}-event-broker-api-service'
    )

    EventBrokerBusStack(
        app,
        "EventBrokerBusStackAppStack",
        stack_name=f'{context.environment}-event-broker-bus'
    )

    return app


build_app().synth()
