import json
import boto3


def handler(event, context):
    request = json.loads(event['body'])
    text = request['text']

    # add comprehend code here
    response = {'result': text}

    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }
