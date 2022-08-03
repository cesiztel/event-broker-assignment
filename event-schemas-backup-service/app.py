#!/usr/bin/env python3

import aws_cdk as cdk
from context import SystemContext

from event_schemas_backup_service.event_schemas_backup_service_stack import EventSchemasBackupServiceStack

def build_app() -> cdk.App:
    """Build the CDK app"""
    context = SystemContext()
    app = cdk.App()

    EventSchemasBackupServiceStack(
        app,
        "EventSchemasBackupServiceStack",
        stack_name=f"{context.environment}-event-schemas-backup-service"
    )

    return app

build_app().synth()
