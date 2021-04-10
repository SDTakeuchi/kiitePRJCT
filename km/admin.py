from django.contrib import admin

# Register your models here.
from .models import *
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm

# admin.site.register(Student)

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email','real_name','student_status', 'is_staff', 'is_active')
    list_filter = ('email','real_name','student_status', 'is_staff', 'is_active')
    readonly_fields = ('id','real_name')
    fieldsets = (
        (None, {'fields': ('name','real_name','email', 'password','introduction')}),
        ('Standard information', {'fields': ('student_status','groups', 'profile_pic','entry_year','industry','job_type')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
        ('Date information', {'fields': ('date_created', 'last_login')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Tag)
admin.site.register(Post)
admin.site.register(Comment)