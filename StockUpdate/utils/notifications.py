import requests
import json


def send_email(receiver, subject, body):
    """_summary_

    Args:
        receiver (_type_): sends emails
        subject (_type_): _description_
        body (_type_): _description_
    """
    url = "https://europe-west2-shad-automation.cloudfunctions.net/notification-email"
    headers = {"Content-Type": "application/json"}
    data = {"receiver": receiver, "subject": subject, "body": body}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response.text)
