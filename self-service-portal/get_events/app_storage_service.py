import boto3
from boto3.dynamodb.conditions import Attr


class SelfServiceStorageService:
    """Service dedicate to interact with the main storage"""
    
    _SK_KEY = "SK"
    _SK_KEY_ATTRIBUTE = "CREATE_EVENT#"

    def __init__(self, table_name):
        self.client = boto3.resource('dynamodb')
        self.table = self.client.Table(table_name)

    def all(self):
        """Get all the ressults from the datastorage"""

        results = []
        last_evaluated_key = None
        filterExpression = Attr(self._SK_KEY).begins_with(self._SK_KEY_ATTRIBUTE)

        while True:
            if last_evaluated_key:
                response = self.table.scan(
                    ExclusiveStartKey=last_evaluated_key,
                    FilterExpression=filterExpression
                )
            else:
                response = self.table.scan(FilterExpression=filterExpression)
            last_evaluated_key = response.get('LastEvaluatedKey')

            results.extend(response['Items'])

            if not last_evaluated_key:
                break
        return results
