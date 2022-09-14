import os
from time import sleep
from .models import Word, User, SendTime
from twilio.rest import Client
from celery import shared_task
from datetime import datetime

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

# sends 5 most recent translations to user's phone
@shared_task(name = "send_daily_words_task")
def send_daily_words_task():
    hour = datetime.now().hour
    send_time = SendTime.objects.get(hour=hour)
    # send texts to all users that want translations by text
        # get current time and iterate through all users who want words at that time
    for user in send_time.user_set.all():
        body_list = []
        # get n oldest words, with n being specified by user in options
        entries = Word.objects.filter(user=user).order_by('saved_date')[:user.num_words]
        # convert translations into string to be sent
        for entry in entries:
            body_list.append(f'{entry.original}: {entry.translation}\n')
            # updates the saved_date value in the word objects
            entry.save()
        body_string = ''.join(body_list)
        # send translations to user using Twilio API
        message = client.messages.create(
                body=body_string,
                from_='+18106311913',
                to=user.phone_number
            )