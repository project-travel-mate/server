from django.db import models
from django.contrib.auth.models import User


class Checklist(models.Model):
    user = models.ForeignKey(User, related_name='checklist', on_delete=models.CASCADE)
    last_updated = models.DateTimeField(auto_now=True)


class ChecklistItem(models.Model):
    checklist = models.ForeignKey('Checklist', related_name='items', on_delete=models.CASCADE)
    item = models.CharField(max_length=20)
