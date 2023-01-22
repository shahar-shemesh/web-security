from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE) ##if user is deleted then delete their posts as well

    def __str__(self):
        return self.title



class NS_user(models.Model):
    name = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    username = models.CharField(max_length=150)
    password = models.CharField(max_length=150)
    email = models.EmailField(max_length=150)

    def __str__(self):
        return self.username

    def get_password(self):
        return self.password

    def set_password(self, password):
        self.password = password

