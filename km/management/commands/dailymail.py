from django.core.management.base import BaseCommand, CommandError
from django.core.mail import EmailMessage
from kiite_me.settings import EMAIL_HOST_USER
from django.template.loader import render_to_string
from datetime import datetime
from km.models import *
import km.views

class Command(BaseCommand):

    def handle(self, *args, **options):

        today1959 = datetime.datetime.now().replace(hour=19,minute=59,second=45, microsecond=0)
        yesterday2000 = today1959 - datetime.timedelta(days=1)
        yesterday2000 = yesterday2000.replace(hour=20,minute=0,second=0, microsecond=0)

        toUser = CustomUser.objects.filter(student_status__contains="卒業生").values_list("email", flat=True)
        posts = Post.objects.all().filter(date_created__gte=yesterday2000).filter(date_created__lte=today1959)

        context ={'posts':posts}
        if posts:
            
            subject = render_to_string('email_template/dailymail/subject.txt', context)
            message = render_to_string('email_template/dailymail/upper_message.txt', context)
            
            for question in posts:
                message += "-----------------------------------------------------"
                message += '\n'
                message += question.user.name 
                message += '\n'
                message += question.title
                message += '\n'
                message += question.body
                message += '\n'
                message += '\n'
            
            message +=render_to_string('email_template/dailymail/lower_message.txt', context)

            # recepient = list(toUser) #in actual page, the mail is delivered to alumni
            recepient = ["123@gmail.com", "abc@gmail.com"] #erace this line for actual environment
            msg = EmailMessage(subject, message, EMAIL_HOST_USER, bcc=recepient)
            msg.send()
