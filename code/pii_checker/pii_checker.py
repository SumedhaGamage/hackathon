import json
import logging
import boto3
from botocore.exceptions import ClientError
from processors import Segmenter, Redactor

logger = logging.getLogger(__name__)


def detect_pii(text, language_code):
    try:
        client = boto3.client('comprehend')
        response = client.detect_pii_entities(
            Text=text, LanguageCode=language_code)
        entities = response['Entities']
        logger.info("Detected %s PII entities.", len(entities))
    except ClientError:
        logger.exception("Couldn't detect PII entities.")
        raise
    else:
        return entities


def handler(event, context):
    request = json.loads(event['body'])
    text = request['text']
    language_code = 'en'
    pii_classification = detect_pii(text, language_code)

    return {
        'statusCode': 200,
        'body': json.dumps(pii_classification)
    }
