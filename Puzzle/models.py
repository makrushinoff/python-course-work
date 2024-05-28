from django.db import models


class Boards(models.Model):
    id = models.BigAutoField(primary_key=True)
    data = models.CharField()

    class Meta:
        db_table = "boards"
