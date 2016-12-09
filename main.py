from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import ecoAuth
import ssl
import boto3
import time
#from boto3 import dynamodb

#dynamodb = boto3.resource('dynamodb')
#table = dynamodb.Table('connectItAllSecrets')

def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")

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
myMQTTClient.subscribe("iot/ecobee/Python", 1, customCallback)
loops = 0
while True:
    myMQTTClient.publish("iot/ecobee/Python", "myPayload"+str(loops), 0)
    loops +=1
    time.sleep(1)
myMQTTClient.disconnect()

