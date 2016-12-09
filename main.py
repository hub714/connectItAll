import ecoAuth
import boto3
from boto3 import dynamodb

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('connectItAllSecrets')
apiKey = ecoAuth.get_api_key()
print ecoAuth.get_current_token(apiKey)
