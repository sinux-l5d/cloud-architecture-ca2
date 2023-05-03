import boto3
import os
import json
from datetime import datetime


def lambda_handler(event, context):
    print(event)
    inp = {
        "id": "1234567890",
        "issuerFullName": "John Doe",
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
