from event_data import EventData


class SchemaDefinition:

    @staticmethod
    def generates(event_data: EventData):
        return {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "title": f'Schema produce for {event_data.unit} for the event {event_data.name}',
            "description": event_data.description,
            "type": "object",
            "properties": {
                "metadata": {
                    "type": "object",
                    "properties": {
                        "parent_id": {
                            "type": "string"
                        },
                        "generated_at": {
                            "type": "string"
                        },
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
