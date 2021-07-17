from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email','real_name','student_status', 'is_staff', 'is_active')
    list_filter = ('email','real_name','student_status', 'is_staff', 'is_active')
    readonly_fields = ('id','real_name')
    fieldsets = (
        (None, {'fields': ('name','real_name','email', 'password','introduction')}),
        ('Standard information', {'fields': ('student_status','groups', 'profile_pic','entry_year','industry','job_type','is_active')}),
        ('Permissions', {'fields': ('is_staff','can_ask')}),
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

class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'ordering_number')

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Article)