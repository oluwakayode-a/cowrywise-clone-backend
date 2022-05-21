from urllib import response
from paystackapi.paystack import Paystack
import os

secret_key = os.environ.get("PAYSTACK_PRIVATE_KEY")

paystack = Paystack(secret_key=secret_key)

def verify_transaction(reference):
    try:
        response = paystack.transaction.verify(reference)
        return True
    except Exception as e:
        print(e)
        return False


def transfer(amount, customer_txn):
    response = paystack.transfer.initiate(
        source="balance",
        reason="Transfer from stash",
        amount=amount,
        recipient=customer_txn,
    )
    return True