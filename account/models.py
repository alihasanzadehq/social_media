from django.contrib.auth.models import User
from django.db import models

class Relation(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='followers')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE,related_name='following')
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.from_user} fallowing {self.to_user}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.PositiveIntegerField(default=0)
    bio = models.TextField(null=True, blank=True)

