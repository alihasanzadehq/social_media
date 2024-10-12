from django.contrib import admin
from .models import Relation ,Profile
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False

class ExtenedUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    

admin.site.unregister(User)
admin.site.register(User,ExtenedUserAdmin)
admin.site.register(Relation)
