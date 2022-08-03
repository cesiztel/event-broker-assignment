import os


class SystemContext:
    def __init__(self) -> None:
        """Construct a new Context class"""
        self.environment = os.environ.get("ENVIRONMENT", "dev")
        self.event_bus_name = os.environ.get("EVENT_BUS_NAME", "custom.events.bus")
        self.account = os.environ.get("ACCOUNT", "756525791342")
        self.region = os.environ.get("REGION", "eu-west-2")
