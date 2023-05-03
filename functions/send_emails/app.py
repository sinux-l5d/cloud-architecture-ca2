import boto3
import os


def lambda_handler(event, context):
    print("mock email sent with", event)

    ses = boto3.client('ses')
    res = ses.send_email(
        Source=os.environ['SES_EMAIL'],
        Destination={
            'ToAddresses': [
                # test purpose, won't be change for this assignment
                "aws-no-reply@sinux.sh"
            ],
        },
        Message={
            'Subject': {
                'Data': 'Ticket creation test',
                'Charset': 'UTF-8'
            },
            'Body': {
                'Text': {
                    'Data': 'Ticket creation body test',
                    'Charset': 'UTF-8'
                }
            }
        }
    )

    # return okey to step function as task
    return {}
