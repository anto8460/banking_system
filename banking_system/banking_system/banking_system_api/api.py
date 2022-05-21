from rest_framework import generics, permissions
from rest_framework.response import Response

from banking_system_api.permissions import IsBankOrNoAccess
from .serializers import AccountSerializer

from banking_system_app.models import Account, Ledger


class HasAccount(generics.RetrieveAPIView):
    permission_classes = [IsBankOrNoAccess, permissions.IsAuthenticated]

    queryset = Account.objects.all()
    serializer_class = AccountSerializer

    def get_queryset(self):
        account_id = self.kwargs['pk']
        queryset = Account.objects.filter(id=account_id)
        return queryset


class CreateTransaction(generics.CreateAPIView):
    permission_classes = [IsBankOrNoAccess, permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        amount = request.data['amount']
        account_id = request.data['account_id']
        text = request.data['text']

        account = Account.objects.get(id=account_id)
        try:
            Ledger.inter_transfer(amount, account, text)
            return Response({"status": "done"})
        except:
            return Response(data={"status": "error"}, status=500)
