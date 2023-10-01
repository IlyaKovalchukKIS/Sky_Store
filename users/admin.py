from django.contrib import admin

from users.models import User, UserBlock

# Register your models here.

admin.site.register(User)


@admin.register(UserBlock)
class UserBlockAdmin(admin.ModelAdmin):
    list_display = ('user', 'is_blocked',)
