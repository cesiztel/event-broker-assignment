import os


class SystemContext:
    def __init__(self) -> None:
        """Construct a new Context class"""
        self.environment = os.environ.get("ENVIRONMENT", "dev")
