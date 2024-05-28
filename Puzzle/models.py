from django.db import models

class Boards(models.Model) :
    id = models.BigAutoField(primary_key=True)
    data = models.CharField()
    class Meta:
        db_table = "boards"
    

class Users(models.Model):
    id = models.AutoField(primary_key=True)
    login = models.CharField(unique=True, max_length=255)
    password = models.CharField()
    class Meta:
        db_table = "users"