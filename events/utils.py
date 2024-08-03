from django.core.mail import send_mail
from django.conf import settings

def send_notification(recipient, subject, message):
    try:
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,  # Ensure this is correctly configured in your settings
            [recipient],  # Pass recipient as a list
            fail_silently=False,  # Adjust fail_silently based on your preference
        )
    except Exception as e:
        print(f"An error occurred while sending email: {e}")
        raise