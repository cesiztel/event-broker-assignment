import boto3
from boto3.dynamodb.conditions import Attr


class SelfServiceStorageService:
    def __init__(self, table_name):
        self.client = boto3.resource('dynamodb')
        self.table = self.client.Table(table_name)

    def all(self):
        results = []
        last_evaluated_key = None
        filterExpression = Attr("SK").begins_with("CREATE_EVENT#")

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
