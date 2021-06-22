from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from users.models import ApiUser, Tier


class ApiUserInline(admin.StackedInline):
    model = ApiUser
    can_delete = False
    verbose_name_plural = 'api users'


class ApiUserAdmin(UserAdmin):
    inlines = [ApiUserInline]


class RoleAdmin(admin.ModelAdmin):
    pass


admin.site.unregister(User)
admin.site.register(User, ApiUserAdmin)
admin.site.register(Tier, RoleAdmin)
