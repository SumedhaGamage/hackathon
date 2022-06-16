import json
import boto3


def handler(event, context):
    request = json.loads(event['body'])

    # add comprehend code here

    return {
        'statusCode': 200,
        'body': json.dumps(request)
    }
