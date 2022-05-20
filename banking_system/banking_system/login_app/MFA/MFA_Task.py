
import django_rq
from SMS_Client.SMS_Client import SMS_Client


def send_code(code, phone_number):
    django_rq.enqueue(_send_code, {'code': code, 'phone_number': phone_number})


def _send_code(params):
    SMS_Client().send_message(params['code'], params['phone_number'])
