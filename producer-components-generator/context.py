import os


class SystemContext:
    def __init__(self) -> None:
        """Construct a new Context class"""
        self.environment = os.environ.get("ENVIRONMENT", "dev")
        self.apigw = os.environ.get("API_GATEWAY_ID", "")
        self.apigw_root_resource = os.environ.get("API_GATEWAY_ROOT_ID", "")
