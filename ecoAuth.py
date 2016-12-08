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
    response = table.put_item(
        Item = {
            'Name': 'authorizationCode',
            #'Value': 'abcd'
            'Value': str(data['code'])
        }
    )
    response = table.put_item(
        Item = {
            'Name': 'ecoBeePin',
            'Value': str(data['ecobeePin'])
        }
    )

def get_access(apiKey):
    response = table.get_item(
        Key={
            'Name': 'authorizationCode'
        }
    )
    authorizationCode = response['Item']['Value']
    url = 'https://api.ecobee.com/token'
    
    payload = {
        'grant_type': 'ecobeePin',
        'code': authorizationCode,
        'client_id': apiKey
    }
    #query_string = 'grant_type=ecobeePin&code='+authorizationCode+'&client_id='+apiKey
    #print url+query_string
    
    response = requests.post(url, data=payload)
    data = response.json()
    print 'Access Token: '+data['access_token']
    print 'Refresh Token: '+data['refresh_token']
    response = table.put_item(
        Item = {
            'Name': 'accessToken',
            'Value': str(data['access_token'])
        }
    )
    response = table.put_item(
        Item = {
            'Name': 'refreshToken',
            'Value': str(data['refresh_token'])
        }
    )

def refresh_access(apiKey):
    response = table.get_item(
        Key={
            'Name': 'refreshToken'
        }
    )
    refreshToken = response['Item']['Value']

    url = 'https://api.ecobee.com/token'

    payload = {
        'grant_type': 'refresh_token',
        'code': refreshToken,
        'client_id': apiKey
    }

    response = requests.post(url, data=payload)
    data = response.json()
    print 'Access Token: '+data['access_token']
    print 'Refresh Token: '+data['refresh_token']
    response = table.put_item(
        Item = {
            'Name': 'accessToken',
            'Value': str(data['access_token'])
        }
    )
    response = table.put_item(
        Item = {
            'Name': 'refreshToken',
            'Value': str(data['refresh_token'])
        }
    )

if __name__ == '__main__':
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('connectItAllSecrets')

    apiKey = get_api_key()
    #initial_auth(apiKey)
    #get_access(apiKey)
    refresh_access(apiKey)
    #pprint.pprint(data)
else:
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('connectItAllSecrets')
    print 'Outside __main__'

