from django.contrib import admin

from django.contrib.auth.admin import UserAdmin

from .models.profile import Profile,Post, Comment, Like
from .models.user import User



@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    pass


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass




