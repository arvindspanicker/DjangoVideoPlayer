# Django imports
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

# Custom imports
from accounts import models
from accounts.forms import UserAdminForm


@admin.register(models.UserModel)
class UserAdmin(UserAdmin):
    list_display = ('id',  'username', 'is_admin')
    list_filter = ('is_admin',)
    form = UserAdminForm
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Fields', {'fields': ('is_admin',)}),
    )



admin.site.unregister(Group)
