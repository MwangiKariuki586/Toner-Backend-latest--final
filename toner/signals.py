# toner_management_app/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from custom_auth.models import Toner_Request,Toner
from django.core.mail import send_mail
import logging
logger = logging.getLogger(__name__)

@receiver(post_save, sender=Toner_Request)
def update_toner_quantity(sender, instance, created, **kwargs):
    if instance.issued and instance.toner:
        instance.toner.quantity -= 1
        instance.toner.save()
@receiver(post_save, sender = Toner)
def notify_low_toner(sender ,instance,created ,**kwargs):
    if instance.quantity <= 3:
        subject = 'Toner Stock Update'
        message = f'Hello, the stock for "{instance.Toner_name}" toner is running low, with only {instance.quantity} left. Kindly replenish.'
        email_from = 'aleqohmwas@gmail.com'
        recipient_list = ['mwangialex268@gmail.com']
        try:
            # Send email
            send_mail(subject, message, email_from, recipient_list, fail_silently=False)
        except Exception as e:
            # Highlight: Logging the email sending issue
             logger.error(f"Error sending email: {e}")