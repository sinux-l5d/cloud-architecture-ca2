import boto3
import os
import json
import uuid
from datetime import datetime


def lambda_handler(event, context):
    print(event)
    # TEST
    return {
        "sessionState": {
            "dialogAction": {
                "type": "Close",
            },
            "intent": {
                "name": event['sessionState']['intent']['name'],
                "state": "Fulfilled",
            },
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": "The ticket creation process has started."
            }
        ],
    }
    intent = event['sessionState']['intent']
    if intent['state'] != 'ReadyForFulfillment' or intent['name'] != 'SubmitIssue':
        return {
            "sessionState": {
                "dialogAction": {
                    "type": "Close",
                },
                "intent": {
                    "state": "Failed",
                },
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": "The ticket creation process has failed."
                }
            ],
        }
    # NOT ACCESSIBLE
    inp = {
        "id": str(uuid.uuid4()),
        "issuerFullName": " ".join(),
        "issuerEmail": "john@doe.org",
        "subject": "runtime",
        "type": "incident",
        "timestamp": datetime.now().isoformat(),
    }

    client = boto3.client('stepfunctions')
    res = client.start_execution(
        stateMachineArn=os.environ['STEP_FUNCTION_ARN'],
        input=json.dumps(inp),
    )
    print(res)

    # for AWS Lex
    return {
        "dialogAction": {
            "type": "Close",
            "fulfillmentState": "Fulfilled",
            "message": {
                "contentType": "PlainText",
                "content": "The ticket creation process has started."
            }
        }
    }

# aws cli command line to invoke a lambda function:
# aws lambda invoke --function-name <function_name> --payload '{"key1": "value1", "key2": "value2", "key3": "value3"}' output.txt
