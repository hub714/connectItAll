#!/bin/bash
mkdir certs
aws s3 cp s3://huberttest/iotproject ./certs/ --recursive
