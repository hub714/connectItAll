import requests 
import boto3
import json
from boto3 import dynamodb

def get_api_key():
    "Need to get API Key from DDB using Role"
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('connectItAllSecrets')

    response = table.get_item(
        Key={
            'Name': 'apiKey'
        }
    )
    item = response['Item']['Value']
    return item



print(get_api_key())
