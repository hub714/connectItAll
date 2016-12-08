import requests 
import boto3
import json
import pprint
from boto3 import dynamodb

def get_api_key():
    "Need to get API Key from DDB using Role"
    #dynamodb = boto3.resource('dynamodb')
    #table = dynamodb.Table('connectItAllSecrets')

    response = table.get_item(
        Key={
            'Name': 'apiKey'
        }
    )
    item = response['Item']['Value']
    return item

def refresh_token(apiKey):
    "Function to refresh the token given an api Key"
    response = table.get_item(
        Key={
            'Name': 'refreshToken'
        }
    )
    refreshToken = response['Item']['Value']
    url = 'https://api.ecobee.com/token'
    query_string = 'grant_type=refresh_token&code='+refreshToken+'&client_id='+apiKey
    response = requests.get(url+query_string)
    data = response.json()
    print data
    return data

def initial_auth(apiKey):
    url = 'https://api.ecobee.com/authorize'
    query_string = '?response_type=ecobeePin&client_id='+apiKey+'&scope=smartWrite'
    #print url+query_string
    response = requests.get(url+query_string)
    data = response.json()
    print 'Authroization Code: '+data['code']
    print 'ecoBee Pin: '+data['ecobeePin'] 

if __name__ == '__main__':
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('connectItAllSecrets')

    apiKey = get_api_key()
    initial_auth(apiKey)
    #pprint.pprint(data)
else:
    print 'Outside __main__'

