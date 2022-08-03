#!/usr/bin/env python3

import aws_cdk as cdk
from producer import ProducerBuilder
from context import SystemContext

from producer_components_generator.producer_components_generator_stack import ProducerComponentsGeneratorStack


def normalize_stack_name(stack_name: str):
    return stack_name.replace("_", "-")


def build_app(producer) -> cdk.App:
    """Build the CDK app"""
    context = SystemContext()
    app = cdk.App()

    # Normalize stack name
    stack_name = normalize_stack_name(
        f"{context.environment}-producer-{producer.event_type}-v{producer.version}"
    )

    ProducerComponentsGeneratorStack(
        app,
        "ProducerComponentsGeneratorStackAppStack",
        producer=producer,
        stack_name=stack_name
    )

    return app


producer = ProducerBuilder.make_producer_from_config_file()
build_app(producer=producer).synth()
