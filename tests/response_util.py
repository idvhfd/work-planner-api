import json


def parse_data(response):
    return json.loads(response.data)['data']


def parse_errors(response):
    return json.loads(response.data)['errors']
