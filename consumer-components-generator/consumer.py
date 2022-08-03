import json

class LambdaConsumerModel:
    def __init__(self, configuration: dict):
        self.configuration = configuration
        self.event_type = configuration.get("event_type")
        self.target_unit = configuration.get("target_unit")
        self.version = configuration.get("version")
        self.connection_type = configuration.get("connection_type")
        self.arn = configuration.get("connection_string")

class ConsumerBuilder:

    @staticmethod
    def make_consumer_from(configuration: dict) -> LambdaConsumerModel:
        """Create a consumer model from the input configuration"""
        connection_type = configuration.get("connection_type")

        # For now only support Lambda
        if connection_type == "LAMBDA":
            return LambdaConsumerModel(configuration)
        # elif connection_type == "SQS":
            # return SqsConsumerModel(configuration)
        # elif connection_type == "SQS":
            # return HttpConsumerModel(configuration)

        raise RuntimeError(f"Unknown connection type {connection_type}")
    
    @classmethod
    def make_consumer_from_config_file(cls):
        """Instantiate a ProducerModel from an input file"""
        consumer_configuration = open('config/deploy.json')

        configuration = json.load(consumer_configuration)
        return cls.make_consumer_from(configuration)