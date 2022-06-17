import datetime
import json
import random
import boto3
from pii_generator.pii_data_generator import PIIGenerator

STREAM_NAME = "ExampleInputStream"
session = boto3.Session(profile_name='jphack')


def generate(text, stream_name, kinesis_client):
    # streams = kinesis_client.list_delivery_streams()
    # print(streams)
    response = kinesis_client.put_record(
        DeliveryStreamName=stream_name,
        Record= {
            'Data': text
        })
    print(response)


if __name__ == '__main__':
    pii_gen = PIIGenerator(how_many=1, both_credit_type=True)
    data = pii_gen.get_data_in_dict()
    for text in data:
        string_value = f"{text['first_name']} {text['last_name']} lives in {text['address']} with personal contact {text['email']} born in {text['dob']} paid for the visit via {text['credit_card']} with number {text['cvv']} "
        print("================= PII Checker Start============")
        print(string_value)
        generate(string_value, "FirehoseStack-PIIDeliveryStreamB11720FD-jT28um84WeOs", session.client('firehose'))
        print("================= PII Checker END============")
