# services.py
from django.core.cache import cache
import random

from social_network.utils.common_utils import generate_otp, print_log
from .. import models

def send_otp(user):
    otp_code = generate_otp()
    # Store OTP in cache with an expiry time (e.g., 10 minutes)
    cache.set(f"otp_{user.email}", otp_code, timeout=300)  # 300 seconds = 5 minutes

    # Integrate with SMS or email service here to send `otp_code`

    print_log(f"OTP for user {user.email}: {otp_code}")

def verify_otp(user, otp_code):
    cached_otp = cache.get(f"otp_{user.email}")
    if cached_otp == otp_code:
        # Invalidate the OTP after successful verification
        cache.delete(f"otp_{user.email}")
        return True
    return False
