from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator
from .managers import CustomUserManager

YEAR_CHOICES = []
for r in range(2016, (datetime.datetime.now().year)):
    YEAR_CHOICES.append((r,r))

def current_year():
    return datetime.date.today().year

def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)    

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    name = models.CharField(max_length=30, null=True)
    real_name = models.CharField(max_length=40)
    profile_pic = models.ImageField(default='profile-icon-png-898.png', null=True, blank=True)
    introduction = models.TextField(max_length=200, default="まだプロフィールを記入していないようです、、、", null=True, blank=True,)
    id = models.BigAutoField(primary_key=True)

    UNDERGRADUATE = '在学生'
    ALUMNIUM = '卒業生'
    STUDENT_STATUS_CHOICES = (
        (UNDERGRADUATE, '在学生'),
        (ALUMNIUM, '卒業生')
    )
    student_status = models.CharField(max_length=3, choices=STUDENT_STATUS_CHOICES)
    #----for-undergraduate-------------
    entry_year = models.IntegerField(_('year'), max_length=4, validators=[MinValueValidator(2016), max_value_current_year], choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    #----for-alumni-------------
    industry = models.CharField(max_length=50, blank=True, null=True)
    job_type = models.CharField(max_length=50, blank=True, null=True)
    #--------------------------------
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(default=timezone.now, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email

class Tag(models.Model):
    name = models.CharField(max_length=20,null=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    title = models.TextField(max_length=150, null=True)
    body = models.TextField(null=True)
    tag = models.ForeignKey(Tag, null=True,on_delete= models.SET_NULL, verbose_name='タグ')
    user = models.ForeignKey(CustomUser,null=True, on_delete= models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(CustomUser,null=True, on_delete= models.SET_NULL)
    body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.post.title, self.user)
         #this is how it is written in python2 mainly,
         #you'd better write return self.post.title + self.user in python3