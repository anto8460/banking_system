from rest_framework import serializers
from banking_system_app.models import Account


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ['id']
        model = Account

