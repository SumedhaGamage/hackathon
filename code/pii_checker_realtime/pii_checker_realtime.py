import json
import logging
import boto3
from botocore.exceptions import ClientError
import base64

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
    output = []
    
    print(event)
    for record in event['records']:
        print(record)
        data = base64.b64decode(record['data']).decode('utf-8').strip()
        print(record)
        
        data_record = {
            'message': data,
        }
        
        output_record = {
            'recordId': record['recordId'],
            'result': 'Ok',
            'data': base64.b64encode(json.dumps(data_record).encode('utf-8')).decode('utf-8')
        }
        
        output.append(output_record)
        
    return {'records': output}
        
