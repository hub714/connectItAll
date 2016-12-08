import ecoAuth
import boto3
from boto3 import dynamodb

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('connectItAllSecrets')
print ecoAuth.get_api_key()
