from event_data import EventData


class SchemaDefinition:

    @staticmethod
    def generates(event_data: EventData):
        return {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "type": "object",
            "properties": {
                "metadata": {
                    "type": "object",
                    "properties": {
                        "event_attributes": {
                            "type": "object",
                            "properties": {
                                "source": {
                                    "type": "string"
                                },
                                "target": {
                                    "type": "string"
                                }
                            },
                            "required": [
                                "source",
                                "target"
                            ]
                        }
                    }
                },
                "data": event_data.schema_properties
            },
            "required": [
                "metadata",
                "data"
            ]
        }
