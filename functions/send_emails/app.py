import boto3
import os


def lambda_handler(event, context):
    print("mock email sent with", event)

    # return okey to step function as task
    return {}
