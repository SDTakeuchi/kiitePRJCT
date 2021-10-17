from django.core.mail import EmailMessage
from kiite_me.settings import EMAIL_HOST_USER, STAFF_EMAIL_LIST
from django.template.loader import render_to_string
from datetime import datetime
from km.models import *
from km.line_notifi import send_msg_to_line

def dailymail():
    today1959 = datetime.datetime.now().replace(hour=19,minute=59,second=45, microsecond=0)
    yesterday2000 = today1959 - datetime.timedelta(days=1)
    yesterday2000 = yesterday2000.replace(hour=20,minute=0,second=0, microsecond=0)

    toUser = CustomUser.objects.filter(student_status__contains="卒業生").values_list("email", flat=True)
    posts = Post.objects.all().filter(date_created__gte=yesterday2000).filter(date_created__lte=today1959)

    context ={'posts':posts}
    if not posts:
        recepient = STAFF_EMAIL_LIST
        subject = "【Kiite-me!】No posts today..."
        message = "You can delete this email."
        msg = EmailMessage(subject, message, EMAIL_HOST_USER, bcc=recepient)
        msg.send()
        print('message has been sent')
    if posts:
        
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
            message += truncate(question.title, 20)
            message += '\n'
            message += truncate(question.body, 80)
            message += '\n'
            message += 'https://kiite-me.site/posts/show/' + str(question.id)
            message += '\n'
            message += '\n'

        message += render_to_string('email_template/dailymail/lower_message.txt')
        # recepient = list(toUser) #in actual page, the mail is delivered to all alumni
        recepient = ["123@gmail.com"] #erace this line for actual environment
        
        msg = EmailMessage(subject, message, EMAIL_HOST_USER, bcc=recepient)
        msg.send()
        print('message has been sent')

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

    #below for remind mail to 在学生 not responding to any answers
    three_days_before1959 = today1959 - datetime.timedelta(days=3)
    four_days_before2000 = yesterday2000 - datetime.timedelta(days=3)
    for post in Post.objects.all():
        commented_user = list(post.comments.filter(post=post).values_list('user__email', flat=True))
        liked_user = list(post.comments.filter(post=post).values_list('like_user_list__email', flat=True))
        if str(post.user) not in liked_user:
            if str(post.user) not in commented_user:
                latest_comment = post.comments.filter(post=post).filter(date_added__gte=four_days_before2000).filter(date_added__lte=three_days_before1959).order_by('-date_added').first()
                if latest_comment is not None:
                    context={'user':post.user, 'post':post}
                    subject = render_to_string('email_template/remind/subject.txt', context)
                    message = render_to_string('email_template/remind/message.txt', context)
                    recepient = str(post.user.email)
                    msg = EmailMessage(subject, message, EMAIL_HOST_USER, [recepient], bcc=[EMAIL_HOST_USER])
                    msg.send()
                    print("remind mail has been sent")
