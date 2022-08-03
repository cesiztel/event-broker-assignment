#!/usr/bin/env python3
import aws_cdk as cdk
from consumer import ConsumerBuilder
from context import SystemContext

from consumer_components_generator.consumer_components_generator_stack import ConsumerComponentsGeneratorStack

def normalize_stack_name(stack_name: str):
    return stack_name.replace("_", "-")

def build_app(consumer) -> cdk.App:
    """Build the CDK app"""
    context = SystemContext()
    app = cdk.App()

    # Normalize stack name
    stack_name = normalize_stack_name(
        f"{context.environment}-consumer-{consumer.event_type}-v{consumer.version}"
    )

    ConsumerComponentsGeneratorStack(
        app,
        "ConsumerComponentsGeneratorStackAppStack",
        consumer=consumer,
        stack_name=stack_name,
        env=cdk.Environment(
            account=context.account,
            region=context.region
        )
    )

    return app

consumer = ConsumerBuilder.make_consumer_from_config_file()
build_app(consumer=consumer).synth()
