#!/bin/bash
mkdir certs
curl https://www.symantec.com/content/en/us/enterprise/verisign/roots/VeriSign-Class%203-Public-Primary-Certification-Authority-G5.pem > certs/root-CA.crt
aws s3 cp s3://huberttest/iotproject certs/ --recursive
