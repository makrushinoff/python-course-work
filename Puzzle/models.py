from django.db import models
from django.contrib.auth.models import AbstractUser


class Boards(models.Model):
    id = models.BigAutoField(primary_key=True)
    data = models.CharField()

    class Meta:
        db_table = "boards"


class Users(AbstractUser):
    login = models.CharField(unique=True, max_length=255)
    password = models.CharField()
    username = None

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = ['password']
