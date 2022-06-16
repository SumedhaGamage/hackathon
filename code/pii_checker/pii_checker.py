import json


def handler(event, context):
    request = json.loads(event['body'])

    # add comprehend code here

    return {
        'statusCode': 200,
        'body': request
    }
