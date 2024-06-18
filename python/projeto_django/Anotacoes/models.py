from django.db import models # type: ignore
from django.contrib.auth.models import User

class Task(models.Model):
    text = models.CharField(max_length=50)
    date = models.DateField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    important = models.BooleanField(default=False) 
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Notation(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'notations'
    
    def __str__(self):
        return self.text[:50] + '...'
