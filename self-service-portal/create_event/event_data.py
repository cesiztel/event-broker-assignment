import json


class EventData:
    """Dto representation of an event"""
    schema_definition = ''

    def __init__(self, application, connection_type, event_type, description, schema_properties):
        self.application = application
        self.connection_type = connection_type
        self.event_type = event_type
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

        application = request_body["application"]
        connection_type = request_body["connection_type"]
        event_type = request_body["event_type"]
        description = request_body["description"] if 'description' in request_body else ""
        schema_properties = request_body["schema"]["properties"]

        return EventData(application, connection_type, event_type, description, schema_properties)
