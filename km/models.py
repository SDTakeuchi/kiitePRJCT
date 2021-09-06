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

for r in range(2016, (datetime.datetime.now().year+1)):
    YEAR_CHOICES.append((r,r))

def current_year():
    return datetime.date.today().year+1

def max_value_current_year(value):
    return MaxValueValidator(current_year())(value)


# Job category refs : https://careergarden.jp/industry/
class AlumniJobParentCategory(models.Model):
    name = models.CharField(max_length=25)
    # date_created = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return self.name


class AlumniJobChildCategory(models.Model):
    name = models.CharField(max_length=25)
    parent = models.ForeignKey(AlumniJobParentCategory, verbose_name="親カテゴリー", on_delete=models.PROTECT)
    # date_created = models.DateTimeField(default=timezone.now, null=True)

    def __str__(self):
        return self.name


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
    entry_year = models.IntegerField(_('year'), validators=[MinValueValidator(2016), max_value_current_year], choices=YEAR_CHOICES, default=datetime.datetime.now().year)
    #----for-alumni-------------
    industry = models.CharField(max_length=50, blank=True, null=True)
    job_type = models.CharField(max_length=50, blank=True, null=True)
    can_ask = models.BooleanField(default=False)
    job_category = models.ForeignKey(AlumniJobChildCategory, verbose_name="業界", blank=True, null=True, default=None, on_delete=models.PROTECT)
    #----for-new-user---------------
    key = models.CharField(max_length=255, unique=True, null=True)
    expiration_date = models.DateTimeField(blank=True, null=True)
    #--------------------------------
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(default=timezone.now, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    bronze = 5
    silver = 20
    gold = 50

    def show_rank(self):
        comment_count = Comment.objects.filter(user=self).count()
        if comment_count >= self.gold:
            return "gold"
        elif comment_count >= self.silver:
            return "silver"
        elif comment_count >= self.bronze:
            return "bronze"
        else:
            return None

    def remaining_comments_to_rankup(self):
        comment_count = Comment.objects.filter(user=self).count()
        current_rank = self.show_rank()
        if current_rank == None:
            return "あと{}回コメントで\nブロンズにランクアップ！".format(self.bronze-comment_count)
        elif current_rank == "bronze":
            return "あと{}回コメントで\nシルバーにランクアップ！".format(self.silver-comment_count)
        elif current_rank == "silver":
            return "あと{}回コメントで\nゴールドにランクアップ！".format(self.gold-comment_count)
        elif current_rank == "gold":
            return "おめでとうございます！\n最高ランクのゴールド達成です！"

    def __str__(self):
        return self.email


class Tag(models.Model):
    name = models.CharField(max_length=20, null=True)
    ordering_number = models.IntegerField(default=0, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['ordering_number']


class Post(models.Model):
    title = models.TextField(max_length=150, null=True)
    body = models.TextField(null=True)
    tag = models.ForeignKey(Tag, null=True,on_delete=models.SET_NULL, verbose_name='タグ')
    user = models.ForeignKey(CustomUser,null=True, on_delete= models.SET_NULL)
    mentioned_user = models.ForeignKey(CustomUser, null=True, blank=True, on_delete= models.SET_NULL, related_name='mentioned_user')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    is_public = models.BooleanField(default=False)
    is_anonymous = models.BooleanField(default=False)
    requested_industry = models.ForeignKey(AlumniJobChildCategory, on_delete=models.SET_NULL, null=True, blank=True)

    def get_comments_count(self):
        return Comment.objects.filter(post=self).count()

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(CustomUser, null=True, on_delete= models.SET_NULL)
    body = models.TextField()
    like_user_list = models.ManyToManyField(CustomUser, blank=True, related_name="like_user_list")
    is_reply_to = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True, default=None)
    date_added = models.DateTimeField(auto_now_add=True)

    def count_like(self):
        return self.like_user_list.count()

    def __str__(self):
        return '%s - %s - %s' % (self.post.title, self.user, self.body[:20])
        #this is how it is written in python2 mainly,
        #you'd better write return self.post.title + self.user in python3

    class Meta:
        ordering = ['date_added']


class Article(models.Model):
    title = models.TextField()
    industry = models.CharField(max_length=20, default=None)
    body = models.TextField(default=None)
    user = models.ForeignKey(CustomUser, null=True, on_delete= models.SET_NULL)
    interviewee_name = models.CharField(max_length=40, null=True, blank=True)
    interviewee_pic = models.ImageField(null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.title

class OfferedJobJoinTable(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    offered_job_parent_category = models.ForeignKey(AlumniJobParentCategory, default=None, on_delete=models.PROTECT)
    offered_job_child_category = models.ForeignKey(AlumniJobChildCategory, default=None, on_delete=models.CASCADE)
    
    def __str__(self):
        return '%s - %s (%s)' % (self.user.name, self.offered_job_child_category, self.offered_job_parent_category)