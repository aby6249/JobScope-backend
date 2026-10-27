from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import EmailMultiAlternatives

from .models import User


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):

   
    if created and instance.is_verified:

        email = instance.email
        username = instance.username

        subject = "Welcome to JobScope"

        text_content = f"""
Welcome to JobScope, {username}!

Your account has been successfully verified.

You can now:

• Discover trusted job platforms
• Improve your resume with AI insights
• Prepare for interviews smarter
• Get career guidance
• Join developer communities

Start your journey today.

— JobScope Team
"""

        html_content = f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Welcome to JobScope</title>
</head>

<body style="margin:0; padding:0; background-color:#f4f7fb; font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,Arial,sans-serif;">

<table width="100%" cellpadding="0" cellspacing="0" style="padding:40px 0;">
<tr>
<td align="center">

<table width="600" cellpadding="0" cellspacing="0"
style="background:white; border-radius:12px; overflow:hidden;
box-shadow:0 10px 30px rgba(0,0,0,0.08);">

<!-- Header -->
<tr>
<td style="background:linear-gradient(135deg,#4f46e5,#7c3aed);
padding:30px; text-align:center;">

<h1 style="color:white; margin:0; font-size:28px;">
Welcome to JobScope
</h1>

<p style="color:#e0e7ff; margin-top:8px;">
Your AI-Powered Developer Career Platform
</p>

</td>
</tr>

<!-- Body -->
<tr>
<td style="padding:40px; color:#1f2937;">

<h2>Hello {username},</h2>

<p style="font-size:16px; line-height:1.6;">
Your account has been successfully verified. You're now part of a platform built to accelerate your developer career.
</p>

<p style="font-size:16px; line-height:1.6;">
JobScope helps you discover opportunities, sharpen your skills, and grow with confidence.
</p>

<!-- Feature Box -->
<div style="background:#f9fafb; border-radius:10px; padding:20px; margin:30px 0;">

<h3 style="margin-top:0;">What you can do now:</h3>

<ul style="line-height:1.8;">
<li>🌐 Discover trusted job platforms</li>
<li>📄 Improve your resume with AI insights</li>
<li>🎯 Prepare for interviews smarter</li>
<li>🤖 Get personalized career guidance</li>
<li>👥 Connect with developer communities</li>
</ul>

</div>

<!-- CTA Button -->
<div style="text-align:center; margin:35px 0;">

<a href="http://localhost:3000"
style="
background:linear-gradient(135deg,#4f46e5,#7c3aed);
color:white;
padding:14px 28px;
text-decoration:none;
border-radius:8px;
font-weight:600;
display:inline-block;
">

Start Exploring JobScope

</a>

</div>

<p>
We're excited to support your growth and help you reach your career goals.
</p>

<p>
Best regards,<br>
<strong>JobScope Team</strong>
</p>

</td>
</tr>

<!-- Footer -->
<tr>
<td style="background:#f9fafb; padding:20px;
text-align:center; font-size:12px; color:#6b7280;">

<p>You received this email because you registered at JobScope.</p>

<p>© 2026 JobScope. All rights reserved.</p>

</td>
</tr>

</table>

</td>
</tr>
</table>

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