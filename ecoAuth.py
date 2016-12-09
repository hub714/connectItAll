import requests 
import time
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

def get_access_token(apiKey):
    currentTime = int(time.time())
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
            'Value': str(data['access_token']),
            'postedAt': str(currentTime)
        }
    )
    response = table.put_item(
        Item = {
            'Name': 'refreshToken',
            'Value': str(data['refresh_token'])
        }
    )
    return data['access_token']

def get_current_token(apiKey):
    response = table.get_item(
        Key={
            'Name': 'accessToken'
        }
    )
    accessToken = response['Item']['Value']

    currentTime = int(time.time())
    #print (currentTime - response['Item']['postedAt'])
    if ((currentTime - response['Item']['postedAt']) > 3300):
        accessToken = refresh_access_token(apiKey)
    return accessToken

def refresh_access_token(apiKey):
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
    #print 'Access Token: '+data['access_token']
    #print 'Refresh Token: '+data['refresh_token']
    
    currentTime = int(time.time())
    response = table.put_item(
        Item = {
            'Name': 'accessToken',
            'Value': str(data['access_token']),
            'postedAt': currentTime
        }
    )
    response = table.put_item(
        Item = {
            'Name': 'refreshToken',
            'Value': str(data['refresh_token'])
        }
    )
    return data['access_token']

if __name__ == '__main__':
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('connectItAllSecrets')

    apiKey = get_api_key()
    #initial_auth(apiKey)
    #get_access_token(apiKey)
    #refresh_access_token(apiKey)
    print get_current_token(apiKey)
    #pprint.pprint(data)
else:
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('connectItAllSecrets')
    print 'Outside __main__'

