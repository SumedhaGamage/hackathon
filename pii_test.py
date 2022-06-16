import http.client
import json
from pii_generator.pii_data_generator import PIIGenerator


def pii_test(text):
    conn = http.client.HTTPSConnection('y3h0hakege.execute-api.us-east-1.amazonaws.com')

    headers = {'Content-type': 'application/json'}
    json_data = json.dumps({'text': text})

    conn.request('POST', '/pii/check', json_data, headers)

    response = conn.getresponse()
    print(response.read().decode())
    # curl - X
    # POST - H
    # "Content-Type: application/json" - d
    # '{"text":"Sumedha Gamage is from USA with zip 77079 phone 444-223-2323 credit card 3333 444555 00777"}'
    # https: // y3h0hakege.execute - api.us - east - 1.
    # amazonaws.com / pii / check


pii_gen = PIIGenerator(how_many=10, both_credit_type=True)
data = pii_gen.get_data_in_dict()
for text in data:
    string_value = f"{text['first_name']} {text['last_name']} lives in {text['address']} with personal contact {text['email']} born in {text['dob']} paid for the visit via {text['credit_card']} with number {text['cvv']} "
    print("================= PII Checker Start============")
    print(string_value)
    pii_test(string_value)
    print("================= PII Checker END============")
