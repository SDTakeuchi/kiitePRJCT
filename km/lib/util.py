import re
from km.models import UserNotification, CustomUser

def regex_get_first_number(string):
    return re.findall('[0-9]+', string)[0]

def regex_get_numbers(string):
    return re.findall('[0-9]+', string)

def truncate(string, length, ellipsis='...'):
    return string[:length] + (ellipsis if string[length:] else '')

def create_user_notification(title, body, recipients, related_post=None):
    """
    receipents can be either STR, LIST, OBJECTS
    """
    notifis = []
    if isinstance(recipients, str):
        notifis.append(UserNotification(
                title = title,
                body = body,
                user = CustomUser.objects.get(email=recipients),
                related_post = related_post
            ))
    else:
        # runs when recipients are LIST type
        for recepient in recipients:
            notifis.append(UserNotification(
                title = title,
                body = body,
                user = CustomUser.objects.get(email=recepient),
                related_post = related_post
            ))

    if notifis is not None:
        UserNotification.objects.bulk_create(notifis)