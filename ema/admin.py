# Importing the libraries
from django.contrib import admin

from ema.models import Comment, Users, Meeting

# Register your models here.

# Comment model with Custom filter in admin
@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_filter=("related_post", "comment_owner",)


# Meeeting model with Custom list of display and filter in admin
@admin.register(Meeting)
class MeetingAdmin(admin.ModelAdmin):
    list_display=("title",)
    list_filter=("owner",)


# Users model with custom list of display in admin
@admin.register(Users)
class UserAdmin(admin.ModelAdmin):
    list_display=("email",)
