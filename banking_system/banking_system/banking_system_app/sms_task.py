
import django_rq
from SMS_Client.SMS_Client import SMSClient


def send_message(message, phone_number):
    django_rq.enqueue(_send_message, {'message': message, 'phone_number': phone_number})


def _send_message(params):
    SMSClient().send_message(params['message'], params['phone_number'])
