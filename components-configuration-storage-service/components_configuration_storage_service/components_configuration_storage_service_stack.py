from aws_cdk import (
    Stack,
    aws_s3 as s3
)
from constructs import Construct
from context import SystemContext

class ComponentsConfigurationConstruct(Construct):
    def __init__(
            self,
            scope: Construct,
            construct_id: str,
            **kwargs
    ) -> None:
        """Construct for the backup bucket"""
        super().__init__(scope, construct_id, **kwargs)
        context = SystemContext()

        # Create Publishers Components storage
        s3.Bucket(
            scope=self,
            id="PublishersBucket", 
            bucket_name=f"{context.environment}-publisher-components-bucket"
        )

        # Create Subscribers Components storage
        s3.Bucket(
            scope=self,
            id="SubscribersBucket", 
            bucket_name=f"{context.environment}-subscriber-components-bucket"
        )

class ComponentsConfigurationStorageServiceStack(Stack):

    def __init__(
        self, 
        scope: Construct, 
        construct_id: str, 
        stack_name: str,
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)
        
        # Initialize the Contruct backup bucket
        ComponentsConfigurationConstruct(
            scope=self,
            construct_id="ComponentsConfigurationConstruct",
            **kwargs
        )
