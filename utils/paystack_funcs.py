from cgitb import reset
from urllib import response
from paystackapi.paystack import Paystack
import os

secret_key = os.environ.get("PAYSTACK_PRIVATE_KEY")

paystack = Paystack(secret_key=secret_key)

def verify_transaction(reference):
    try:
        response = paystack.transaction.verify(reference)
        return response
    except Exception as e:
        print(e)
        return False


def transfer(amount, recipient_code):
    response = paystack.transfer.initiate(
        source="balance",
        reason="Transfer from stash",
        currency="NGN",
        amount=amount,
        recipient=recipient_code,
    )
    return response

def verify_nuban(nuban, bank):
    response = paystack.verification.verify_account(account_number=nuban, bank_code=bank)
    return response

def create_transfer_recipient(name, nuban, bank_code):
    response = paystack.transferRecipient.create(
        name=name,
        type="nuban",
        description=f"Recipient - {name}",
        account_number=nuban,
        bank_code=bank_code
    )
    return response