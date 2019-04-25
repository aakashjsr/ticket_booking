import os
import sendgrid

from django.contrib.auth.models import User

from sendgrid.helpers.mail import *


def get_user(email, first_name):
    """
    Gets or creates a new user with the given email
    :param email: email of user
    :param first_name: first name of user
    :return: user object
    """
    user, _ = User.objects.get_or_create(username=email, defaults={
        "email": email,
        "first_name": first_name
    })
    return user


def send_booking_email(seat):
    """
    Send transactional email when booking is successful
    :param seat: instance of the booked seat
    :return: Boolean - indicating if the email was sent
    """
    message = Mail(
    from_email='booking@seat-booker.com',
    to_emails=seat.booked_by.email,
    subject='Seat booking successful',
    html_content='Your seat with id #{} has been booked successfuly'.format(seat.id))
    sg = sendgrid.SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    try:
        response = sg.send(message)
    except:
        return False
    else:
        return response.status_code == 202
