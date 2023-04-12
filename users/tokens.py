from django.core.mail import send_mail
import random
import string


def create_random_string():
    characters = string.ascii_letters + string.digits + '-'
    random_string = ''.join(random.choice(characters) for i in range(50))
    return random_string


def send_activation_code(email, activation_code):
    activation_url = f'http://localhost:8000/users/registration/activate/{activation_code}'
    message = f'Thank you for signing up. Please activate your account.' \
              f'Please follow the link below: {activation_url}'\
              f'Your activation token is {activation_code}'
    send_mail('Activate your account',
              message,
              'registration@admin.com',
              [email, ],
              fail_silently=False
              )
