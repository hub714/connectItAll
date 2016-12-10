from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient 
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTShadowClient
import ecoAuth
import ssl
import boto3
import time
import json
#from boto3 import dynamodb

# Some Variables
rootCAPath = 'certs/root-CA.crt'
privateKeyPath = 'certs/ecobee.private.key'
certificatePath = 'certs/ecobee.cert.pem'
iotHost = 'a3b5boi1z5frj2.iot.us-west-2.amazonaws.com'

def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")


def initMqtt():

    myMQTTClient = AWSIoTMQTTClient("ecobee")
    myMQTTClient.configureEndpoint(iotHost, 8883)
    myMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

    myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
    myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
    myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
    myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec
    return myMQTTClient

def listenAndSend():
    myMQTTClient = initMqtt()
    myMQTTClient.connect()

    myMQTTClient.subscribe("iot/ecobee/Python", 1, customCallback)
    loops = 0
    while True:
        myMQTTClient.publish("iot/ecobee/Python", "myPayload"+str(loops), 0)
        loops +=1
        time.sleep(1)
    myMQTTClient.disconnect()

# Shadow Stuff

def customShadowCallback_Delta(payload, responseStatus, token):
    # payload is a JSON string ready to be parsed using json.loads(...)
    # in both Py2.x and Py3.x
    print(responseStatus)
    payloadDict = json.loads(payload)
    print("++++++++DELTA++++++++++")
    print("property: " + str(payloadDict))
    #print("version: " + str(payloadDict["version"]))
    print("+++++++++++++++++++++++\n\n")

def initShadow():
    myAWSIoTMQTTShadowClient = None
    myAWSIoTMQTTShadowClient = AWSIoTMQTTShadowClient("ecobee")
    myAWSIoTMQTTShadowClient.configureEndpoint(iotHost, 8883)
    myAWSIoTMQTTShadowClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

    myAWSIoTMQTTShadowClient.configureAutoReconnectBackoffTime(1, 32, 20)
    myAWSIoTMQTTShadowClient.configureConnectDisconnectTimeout(10)  # 10 sec
    myAWSIoTMQTTShadowClient.configureMQTTOperationTimeout(5)  # 5 sec
    return myAWSIoTMQTTShadowClient

def useShadow():
    #jsonPayload['state']['desired']['property'] = 10
    #json.dumps(jsonPayload)
    myAWSIoTMQTTShadowClient = initShadow()
    myAWSIoTMQTTShadowClient.connect()

    # Create a deviceShadow with persistent subscription
    Bot = myAWSIoTMQTTShadowClient.createShadowHandlerWithName("Bot", True)
    Bot.shadowUpdate(jsonPayload, customShadowCallback_Delta, 5)
    #Bot.shadowRegisterDeltaCallback(customShadowCallback_Delta)
    loops = 0
    jsonPayload = {}
    jsonPayload = '{"state": {"desired": {"property":"10"}}}'
    print jsonPayload
    while True:
        Bot.shadowUpdate(jsonPayload, customShadowCallback_Delta, 5)
        loops += 1
        time.sleep(2)

if __name__ == '__main__':
    #listenAndSend()
    apiKey = ecoAuth.get_api_key()
    currentToken = ecoAuth.get_current_token(apiKey)
    print "Current Token: " + currentToken   
    #useShadow()
else:
    print "Not In Main"

