import json


class SubscriptionData:
    """Dto representation of a subscription"""

    def __init__(self, event_type, version, target_unit, connection_type, connection_string):
        self.event_type = event_type
        self.version = version
        self.target_unit = target_unit
        self.connection_type = connection_type
        self.connection_string = connection_string

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4).encode('UTF-8')

    @staticmethod
    def from_request(request):
        """Factory method to create a dto object from the request"""

        request_body = json.loads(request["body"])

        event_type = request_body["event_type"]
        version = request_body["version"]
        target_unit = request_body["target_unit"]
        connection_type = request_body["connection_type"]
        connection_string = request_body["connection_string"]

        return SubscriptionData(event_type, version, target_unit, connection_type, connection_string)
