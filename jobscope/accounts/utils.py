import random
import json

from django.core.mail import EmailMultiAlternatives
from django.conf import settings

from .redis_client import redis_client


# otp gen
def generate_otp():
    return str(random.randint(100000, 999999))

# otp storing
def store_otp_data(email, username, password, otp):

    key = f"otp:{email}"

    data = {
        "username": username,
        "password": password,
        "otp": otp
    }

    print(f"OTP: {otp}")
# redis storing
    redis_client.setex(
        key,
        600,
        json.dumps(data)
    )

# take otp from redis
def get_otp_data(email):

    key = f"otp:{email}"

    data = redis_client.get(key)

    if data:
        return json.loads(data)

    return None


# delte from redis
def delete_otp_data(email):

    key = f"otp:{email}"

    redis_client.delete(key)


# otp tem
def send_otp_email(email, otp):

    subject = "Your JobScope OTP Code"

    text_content = f"""
Hello,

Thank you for registering! Please use the following OTP to verify your email address:

OTP Code: {otp}

This code will expire in 10 minutes.

If you did not request this, please ignore this email.

Best regards,
JobScope Team
"""

    html_content = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>OTP Verification</title>
</head>

<body style="font-family: Arial, sans-serif; background-color: #f4f6f8; padding: 20px;">

<div style="max-width: 500px; margin: auto; background: white; padding: 20px; border-radius: 8px;">

<h2 style="color: #333;">Welcome to JobScope!</h2>

<p style="color: #555;">
Thank you for registering. Please use the OTP below to verify your email address:
</p>

<div style="background: #f1f3f5; padding: 15px; text-align: center; font-size: 28px; letter-spacing: 5px; font-weight: bold; border-radius: 6px;">
{otp}
</div>

<p style="color: #777; margin-top: 15px;">
This code will expire in <b>10 minutes</b>.
</p>

<p style="color: #777;">
If you did not request this, please ignore this email.
</p>

<p style="margin-top: 20px;">
Best regards,<br>
<b>JobScope Team</b>
</p>

</div>

</body>
</html>
"""

    email_message = EmailMultiAlternatives(
        subject,
        text_content,
        settings.EMAIL_HOST_USER,
        [email]
    )

    email_message.attach_alternative(html_content, "text/html")

    email_message.send()




def store_reset_otp(email, otp):
    redis_client.setex(f"reset_otp:{email}", 600, otp)


def get_reset_otp(email):
    return redis_client.get(f"reset_otp:{email}")


def delete_reset_otp(email):
    redis_client.delete(f"reset_otp:{email}")