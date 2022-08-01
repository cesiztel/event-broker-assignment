import json


class EventData:
    """Dto representation of an event"""
    schema_definition = ''

    def __init__(self, unit, name, description, schema_properties):
        self.unit = unit
        self.name = name
        self.description = description
        self.schema_properties = schema_properties

    def attachSchemaContract(self, schema_definition):
        self.schema_definition = schema_definition

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4).encode('UTF-8')

    @staticmethod
    def from_request(request):
        """Factory method to create a dto object from the event"""

        request_body = json.loads(request["body"])

        unit = request_body["unit"]
        name = request_body["name"]
        description = request_body["description"] if 'description' in request_body else ""
        schema_properties = request_body["schema"]["properties"]

        return EventData(unit, name, description, schema_properties)
