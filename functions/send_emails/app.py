import boto3
import os
from datetime import datetime as dt


def lambda_handler(event, context):
    ses = boto3.client('ses')
    res = ses.send_email(
        Source=os.environ['SES_EMAIL'],
        Destination={
            'ToAddresses': [
                # test purpose, won't be change for this assignment
                # not a "customer" email because my AWS SES account is in sandbox mode
                # https://docs.aws.amazon.com/ses/latest/dg/request-production-access.html
                os.environ['SES_EMAIL'],
            ],
        },
        Message={
            'Subject': {
                'Data': 'Ticket creation from ' + event["issuerFullName"],
                'Charset': 'UTF-8'
            },
            'Body': {
                'Text': {
                    'Data': "\n".join([
                        f"Ticket creation from {event['issuerFullName']} submitted on {dt.fromisoformat(event['timestamp']).strftime('%d/%m/%Y at %H:%M')}",
                        f"The {event['type']} is about {event['subject']}",
                        f"This ticket id is {event['id']}",
                        "",
                        "Please reply to this email to ask the customer for more information."
                    ]),
                    'Charset': 'UTF-8'
                }
            }
        },
        ReplyToAddresses=[
            event["issuerEmail"],
        ]
    )

    # return okey to step function as task
    return event
