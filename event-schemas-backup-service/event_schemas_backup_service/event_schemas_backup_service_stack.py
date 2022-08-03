from aws_cdk import (
    Stack,
    aws_s3 as s3
)
from constructs import Construct
from context import SystemContext

class EventSchemasBackupConstruct(Construct):
    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            **kwargs
    ) -> None:
        """Construct for the backup bucket"""
        super().__init__(scope, construct_id, **kwargs)
        context = SystemContext()

        # Create backup bucket
        s3.Bucket(
            scope=self,
            id="Bucket", 
            bucket_name=f"{context.environment}-event-schemas-backup-bucket"
        )

class EventSchemasBackupServiceStack(Stack):

    def __init__(
        self, 
        scope: Construct, 
        construct_id: str, 
        stack_name: str,
        **kwargs
    ) -> None:
        """Construct for the service"""
        super().__init__(scope, construct_id, stack_name=stack_name, **kwargs)

        # Initialize the Contruct backup bucket
        EventSchemasBackupConstruct(
            scope=self,
            construct_id="EventSchemasBackupConstruct",
            **kwargs
        )