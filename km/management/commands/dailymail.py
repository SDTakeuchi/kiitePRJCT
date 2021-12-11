from django.core.management.base import BaseCommand, CommandError
from django.core.mail import EmailMessage
from kiite_me.settings import EMAIL_HOST_USER
from django.template.loader import render_to_string
from datetime import datetime
from lib.util import create_user_notification
from km.models import *
from kiite_me.settings import STAFF_EMAIL_LIST
# from km.line_notifi import send_msg_to_line



class Command(BaseCommand):

    def handle(self, *args, **options):

        today1959 = datetime.datetime.now().replace(hour=19,minute=59,second=45, microsecond=0)
        yesterday2000 = today1959 - datetime.timedelta(days=1)
        yesterday2000 = yesterday2000.replace(hour=20,minute=0,second=0, microsecond=0)

        toUser = CustomUser.objects.filter(student_status__contains="卒業生").values_list("email", flat=True)
        posts = Post.objects.all().filter(date_created__gte=yesterday2000).filter(date_created__lte=today1959).filter(mentioned_user__isnull=True)
        context ={'posts':posts}

        if not posts:
            recepient = [STAFF_EMAIL_LIST]
            subject = "【Kiite-me!】No posts today..."
            message = "You can delete this email."
            msg = EmailMessage(subject, message, EMAIL_HOST_USER, bcc=recepient)
            msg.send()
        elif posts:        
            subject = render_to_string('email_template/dailymail/subject.txt', context)
            message = render_to_string('email_template/dailymail/upper_message.txt', context)
            
            def truncate(string, length, ellipsis='...'):
                '''文字列を切り詰める
                string: 対象の文字列
                length: 切り詰め後の長さ
                ellipsis: 省略記号
                '''
                return string[:length] + (ellipsis if string[length:] else '')

            for question in posts:
                message += "-----------------------------------------------------"
                message += '\n'
                message += question.user.name 
                message += '\n'
                message += truncate(question.title, 24)
                message += '\n'
                message += truncate(question.body, 90)
                message += '\n'
                message += 'https://kiite-me.site/posts/show/' + str(question.id)
                message += '\n'
                message += '\n'

            message += render_to_string('email_template/dailymail/lower_message.txt')
            recepient = list(toUser)

            create_user_notification(
                title=subject[11:], # eliminates 【Kiite-me!】
                body=message,
                recipients=recepient,
                # related_post=post
            )

            message += render_to_string('email_template/base/base_msg.txt')

            msg = EmailMessage(subject, message, EMAIL_HOST_USER, bcc=recepient)
            msg.send()

            #below for LINE
            msg_for_line = "【Kiite-me!】に本日届いた質問をお送りします！ご確認お願いします！\n"
            for question in posts:
                msg_for_line += "---------------------------------------"
                msg_for_line += '\n'
                msg_for_line += question.user.name 
                msg_for_line += '\n'
                msg_for_line += truncate(question.title, 23)
                msg_for_line += '\n\n'
                msg_for_line += truncate(question.body, 90)
                msg_for_line += '\n'
                msg_for_line += 'https://kiite-me.site/posts/show/' + str(question.id)
                msg_for_line += '\n'
                msg_for_line += '\n'
            msg_for_line += "---------------------------------------"
            # send_msg_to_line(msg_for_line)

        #below for remind mail to grad not responding to any answers
        three_days_before1959 = today1959
        four_days_before2000 = yesterday2000
        i=1
        for post in Post.objects.all():
            commented_user = list(post.comments.filter(post=post).values_list('user__email', flat=True))
            print(i)
            i += 1
            print(commented_user)
            liked_user = list(post.comments.filter(post=post).values_list('like_user_list__email', flat=True))
            print(liked_user)
            if str(post.user) not in liked_user and str(post.user) not in commented_user:
                latest_comment = post.comments.filter(post=post).filter(date_added__gte=four_days_before2000).filter(date_added__lte=three_days_before1959).order_by('-date_added').first()
                if latest_comment is not None:
                    print('=================')
                    print(latest_comment)
                    context={'user':post.user, 'post':post}
                    subject = render_to_string('email_template/remind/subject.txt', context)
                    message = render_to_string('email_template/remind/message.txt', context)
                    recepient = str(post.user.email)

                    create_user_notification(
                        title=subject[11:], # eliminates 【Kiite-me!】
                        body=message,
                        recipients=recepient,
                        related_post=post
                    )

                    message += render_to_string('email_template/base/base_msg.txt')

                    msg = EmailMessage(subject, message, EMAIL_HOST_USER, [recepient], bcc=[EMAIL_HOST_USER])
                    msg.send()
                    print("remind mail has been sent")