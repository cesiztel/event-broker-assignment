#!/usr/bin/env python3
import os

import aws_cdk as cdk
from context import SystemContext

from components_configuration_storage_service.components_configuration_storage_service_stack import ComponentsConfigurationStorageServiceStack

def build_app() -> cdk.App:
    """Build the CDK app"""
    context = SystemContext()
    app = cdk.App()

    ComponentsConfigurationStorageServiceStack(
        app,
        "ComponentsConfigurationStorageServiceStack",
        stack_name=f"{context.environment}-components-configuration-storage-service"
    )

    return app

build_app().synth()
