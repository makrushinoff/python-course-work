from django.db import models

class Boards(models.Model) :
    id = models.AutoField(primary_key=True)
    data = models.CharField()
    

class Users(models.Model):
    id = models.AutoField(primary_key=True)
    login = models.CharField(unique=True)
    password = models.CharField()