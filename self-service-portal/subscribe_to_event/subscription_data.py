import json


class SubscriptionData:
    """Dto representation of a subscription"""

    def __init__(self, unit, name, version):
        self.unit = unit
        self.name = name
        self.version = version

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4).encode('UTF-8')

    @staticmethod
    def from_request(request):
        """Factory method to create a dto object from the request"""

        request_body = json.loads(request["body"])
        request_path_parameters = request["pathParameters"]

        unit = request_body["unit"]
        name = request_path_parameters["eventName"]
        version = request_path_parameters["eventVersion"]

        return SubscriptionData(unit, name, version)
