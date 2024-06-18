from django.db import models

# Create your models here.
class Users(models.Model):
    name = models.CharField(max_length=80)
    email = models.EmailField(max_length=70)
    password = models.CharField(max_length=50)

    def __str__(self):
        return self.name
