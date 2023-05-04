import boto3
import os
import json
import uuid
from datetime import datetime


def lexResponse(intentName: str, state: str, message: str):
    return {
        "sessionState": {
            "dialogAction": {
                "type": "Close",
            },
            "intent": {
                "name": intentName,
                "state": state,
            },
        },
        "messages": [
            {
                "contentType": "PlainText",
                "content": message
            }
        ],
    }


def lexFulfilled(intentName: str):
    return lexResponse(intentName, "Fulfilled", "The ticket is being processed.")


def lexFailed(intentName: str):
    return lexResponse(intentName, "Failed", "Sorry, the ticket creation process has failed.")


def lambda_handler(event, context):

    intent = event['sessionState']['intent']

    if intent['state'] != 'ReadyForFulfillment' or intent['name'] != 'SubmitIssue':
        return lexFailed(intent['name'])

    value = lambda x: intent['slots'][x]["value"]['interpretedValue']

    req = {
        "id": str(uuid.uuid4()),
        "issuerFullName": value("FirstName") + " " + value("LastName"),
        "issuerEmail": value("Email"),
        "subject": value("Subject"),
        "type": value("Type"),
        "timestamp": datetime.now().isoformat(),
    }

    client = boto3.client('stepfunctions')
    res = client.start_execution(
        stateMachineArn=os.environ['STEP_FUNCTION_ARN'],
        input=json.dumps(req),
    )

    print(res)

    return lexFulfilled(intent['name'])
