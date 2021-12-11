from django import template
from km.models import UserNotification

register = template.Library()

@register.simple_tag
def show_unread_notifi_num(user):
    notifis = UserNotification.objects.filter(
        user=user,
        is_seen=False
    )
    if notifis:
        return len(notifis)
    else:
        return 0