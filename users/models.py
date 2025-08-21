from django.db import models


class User(models.Model):
    id = id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50)

    def __str__(self):
        return str(self.name)

# Create your models here.
