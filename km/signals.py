# # from django.contrib.auth.models import User
# from django.contrib.auth.models import Group
# from django.db.models.signals import post_save
# from .models import CustomUser

# def student_profile(sender, instance, created, **kwargs):
#     if created:
#         group, created = Group.objects.get_or_create(name='在学生')
#         instance.groups.add(group)

#         CustomUser.objects.create(
#         #     # user=instance,
#         #     name=instance.name,
#         #     email=instance.email
#         #     #when these parameters were in views.py,
#         #     #they were written as user.username/user.groups.add(group),
#         #     #So here, 'user' turned into 'instance'
#         # )

# post_save.connect(student_profile, sender=CustomUser)