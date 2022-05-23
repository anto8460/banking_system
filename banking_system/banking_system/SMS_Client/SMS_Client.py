
from twilio.rest import Client
from decouple import config


class SMSClient:

    def __init__(self):
        self.account_sid = config('ACCOUNT_SID')
        self.auth_token = config('AUTH_TOKEN')
        self.phone_number = config('PHONE_NUMBER')
        self.twilio_client = Client(self.account_sid, self.auth_token)

    def send_message(self, message: str, reciever: str) -> None:
        message = self.twilio_client.messages.create(
            body=message,
            from_=self.phone_number,
            to=reciever)
