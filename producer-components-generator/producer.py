import json


class HttpsProducerModel:
    def __init__(self, configuration: dict):
        self.configuration = configuration
        self.application = configuration.get("application")
        self.event_type = configuration.get("event_type")
        self.version = configuration.get("version")
        self.schema = configuration.get("schema")


class ProducerBuilder:

    @staticmethod
    def make_producer_from(configuration: dict) -> HttpsProducerModel:
        """Create a producer model from the input configuration"""
        connection_type = configuration.get("connection_type")

        # For now only support HTTPS
        if connection_type == "HTTPS":
            return HttpsProducerModel(configuration)
        # if connection_type == "SQS":
            # return SqsProducerModel(configuration)

        raise RuntimeError(f"Unknown connection type {connection_type}")

    @classmethod
    def make_producer_from_config_file(cls):
        """Instantiate a ProducerModel from an input file"""
        producer_configuration = open('config/deploy.json')

        configuration = json.load(producer_configuration)
        return cls.make_producer_from(configuration)
