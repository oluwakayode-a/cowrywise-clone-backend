from pyotp import TOTP

otp = TOTP("base32secret3232", interval=300)

def generate_otp():
    generated_otp = otp.now()

    return generated_otp


def verify_otp(token):
    if otp.verify(token):
        return True
    else:
        False