from django.contrib import admin
from .models import Post, NS_user
from .hashers import PBKDF2WrappedSHA1PasswordHasher

# Register your models here.

admin.site.register(Post)
admin.site.register(NS_user)
