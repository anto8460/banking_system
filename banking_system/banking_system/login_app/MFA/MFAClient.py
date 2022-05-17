
from twilio.rest import Client
from decouple import config
from random import randint


class MFAClient():

    def __init__(self):
        self.account_sid = config('ACCOUNT_SID')
        self.auth_token = config('AUTH_TOKEN')
        self.phone_number = config('PHONE_NUMBER')
        self.twilio_client = Client(self.account_sid, self.auth_token)

    def send_message(self, message, reciever):
        message = self.twilio_client.messages.create(
            body=message,
            from_=self.phone_number,
            to=reciever)

        print(message)

    @staticmethod
    def generate_code() -> str:
        # Generate random code
        return str(randint(100_000, 999_999))
