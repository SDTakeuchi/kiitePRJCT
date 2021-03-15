from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django import  forms
from .models import *


# maybe not needed anymore
class StudentForm(ModelForm):
    class Meta: 
        model = CustomUser
        fields = '__all__'
        exclude = ['user']

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('real_name','name','email','entry_year','industry', 'job_type','student_status')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('real_name','name','email','profile_pic','industry', 'job_type', 'introduction')

class PostForm(ModelForm):
    class Meta:
        model = Post
        fields = ['title','tag', 'body',]

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body',]

# class CreateUserForm(UserCreationForm):
#     class Meta:
#         model = User
#         fields = ['username', 'email', 'password1','password2']

class ContactForm(forms.Form):
    toEmail = forms.EmailField()
    title = forms.fields.ChoiceField(
        choices = (
            ('お問い合わせ内容：お問い合わせ', 'お問い合わせ'),
            ('お問い合わせ内容：通報', '通報'),
            ('お問い合わせ内容：改善の要望', '改善の要望'),
        ),
        required=True,
        widget=forms.widgets.Select
    )
    body = forms.CharField(widget=forms.Textarea)

    def __str__(self):
        return self.toEmail
        
class adminNotificationForm(forms.Form):
    toGroup= forms.fields.ChoiceField(
        choices = (
            ('ユーザーの皆様', '全てのユーザー'),
            ('ユーザー（在学生）の皆様', '在学生'),
            ('ユーザー（卒業生）の皆様', '卒業生'),
            ('スタッフの皆様', 'スタッフへの連絡'),
        ),
        required=True,
        widget=forms.widgets.Select
    )
    title = forms.CharField()
    body = forms.CharField(widget=forms.Textarea)

    def __str__(self):
        return self.title
