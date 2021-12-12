from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django import  forms
from .models import *

User = get_user_model()

# maybe not needed anymore
class StudentForm(ModelForm):
    job_parent_category = forms.ModelChoiceField(
        label='親カテゴリー',
        queryset=AlumniJobParentCategory.objects,
        required=False
        )

    class Meta: 
        model = CustomUser
        fields = '__all__'
        exclude = ['user']

class CustomUserCreationForm(UserCreationForm):
    job_parent_category = forms.ModelChoiceField(
        label='親カテゴリー',
        queryset=AlumniJobParentCategory.objects,
        required=False
        )

    class Meta(UserCreationForm):
        model = CustomUser
        fields = ('real_name','name','email','entry_year','industry', 'job_type','job_parent_category', 'job_category','student_status')

    def clean_email(self):
        email = self.cleaned_data['email']
        User.objects.filter(email=email, is_active=False).delete()
        return email

class CustomUserChangeForm(UserChangeForm):
    job_parent_category = forms.ModelChoiceField(
        label='親カテゴリー',
        queryset=AlumniJobParentCategory.objects,
        required=False
        )
        
    class Meta:
        model = CustomUser
        fields = ('real_name','name','email','entry_year','profile_pic','industry', 'job_type','job_parent_category', 'job_category', 'introduction','can_ask')

# class OfferedJobForm(UserChangeForm):
#     job_parent_category = forms.ModelChoiceField(
#         label='親カテゴリー',
#         queryset=AlumniJobParentCategory.objects,
#         required=False
#         )
        
#     class Meta:
#         model = OfferedJobJoinTable
#         fields = ('job_parent_category', 'offered_job_category',)

class PostForm(ModelForm):
    job_parent_category = forms.ModelChoiceField(
        label='親カテゴリー',
        queryset=AlumniJobParentCategory.objects,
        required=False
        )

    class Meta:
        model = Post
        fields = ['title','tag', 'body','is_public', 'user_is_anonymous', 'job_parent_category', 'requested_industry']

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ['body',]

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

OfferedJobFormset = forms.inlineformset_factory(
        parent_model = CustomUser,
        model = OfferedJobJoinTable,
        fields = ('offered_job_child_category', 'offered_job_parent_category'),
        extra = 3,
        max_num = 3,
        can_delete=True,
    )