from django.db import models
from django.contrib.auth.models import AbstractUser
from .tokens import create_random_string
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail

from django.contrib.postgres.fields import ArrayField


# Create your models here.
class TrelloUser(AbstractUser):
    activation_code = models.CharField(max_length=50, default=create_random_string)
    last_seen = ArrayField(models.IntegerField(), max_length=6, blank=True, null=True)


@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    email_plaintext_message = "{}?token={}".format(reverse('password_reset:reset-password-request'),
                                                   reset_password_token.key)

    send_mail(
        "Password Reset for {title}".format(title="Some website title"),
        email_plaintext_message,
        "noreply@somehost.local",
        [reset_password_token.user.email]
    )

