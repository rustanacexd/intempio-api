from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Role


@admin.register(User)
class UserAdmin(UserAdmin):
    pass


class UsersInline(admin.TabularInline):
    model = User.roles.through


class RolesAdmin(admin.ModelAdmin):
    inlines = [UsersInline]


admin.site.register(Role, RolesAdmin)
