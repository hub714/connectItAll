from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import ecoAuth
import ssl
import boto3
#from boto3 import dynamodb

#dynamodb = boto3.resource('dynamodb')
#table = dynamodb.Table('connectItAllSecrets')
apiKey = ecoAuth.get_api_key()
print ecoAuth.get_current_token(apiKey)

myMQTTClient = AWSIoTMQTTClient("ecobee")
myMQTTClient.configureEndpoint("a3b5boi1z5frj2.iot.us-west-2.amazonaws.com", 8883)
myMQTTClient.configureCredentials("certs/root-CA.crt", "certs/ecobee.private.key", "certs/ecobee.cert.pem")

myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

myMQTTClient.connect()
myMQTTClient.publish("myTopic", "myPayload", 0)
myMQTTClient.disconnect()

