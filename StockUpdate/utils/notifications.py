import requests
import json


def send_email(receiver, subject, body):
    """sends email

    Args:
        receiver (str): receiver email
        subject (str): _subject_
        body (str): _body_
    """
    url = "https://europe-west2-shad-automation.cloudfunctions.net/notification-email"
    headers = {"Content-Type": "application/json"}
    data = {"receiver": receiver, "subject": subject, "body": body}
    response = requests.post(url, headers=headers, data=json.dumps(data))
    print(response.text)
