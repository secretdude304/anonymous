from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class post(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class comment(models.Model):
    postid = models.IntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)
    text = models.CharField(max_length=140)


class User(AbstractUser):
    school = models.ForeignKey(
        "school", on_delete=models.CASCADE, default=True)


class school(models.Model):
    name = models.CharField(max_length=140)
