from django.core.cache import cache
import random

from social_network.models.user_model import User
from social_network.utils.common_utils import generate_otp, print_log
from social_network.utils.mail_utils import send_email
from .. import models
from ..constants import welcome_template, otp_template


def send_otp(email):
    # generate otp
    otp_code = generate_otp()

    # Store OTP in cache with an expiry time (e.g., 5 minutes)
    cache.set(f"otp_{email}", otp_code, timeout=300)  # 300 seconds = 5 minutes

    # print in console if debugging is on
    print_log(f"OTP for user {email}: {otp_code}")

    # send email
    is_send = send_email(
        email,
        otp_template.get_subject(),
        otp_template.get_message(otp=otp_code),
    )

    return is_send


def verify_otp(email, otp_code):
    cached_otp = cache.get(f"otp_{email}")
    if cached_otp == otp_code:
        # Invalidate the OTP after successful verification
        cache.delete(f"otp_{email}")
        return True
    return False


def sign_up(first_name, last_name, email):
    # create user
    user = User.objects.create(
        first_name=first_name, last_name=last_name, email=email, roles=[2]
    )

    # send welcome email
    send_email(
        email,
        welcome_template.get_subject(),
        welcome_template.get_message(
            first_name=user.first_name, full_name=f"{user.first_name} {user.last_name}"
        ),
    )

    # return user
    return user
