debit = Account.objects.get(id="c22f394d-0bea-465a-9b36-0ff92dee06c8")
credit = Account.objects.get(id="031625b0-a50a-4aa4-a6bb-5b48bacb2644")

Ledger.transfer(10_000_000, debit, "Initial transfer", credit, "Initial transfer", is_loan=True)