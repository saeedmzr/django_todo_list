import datetime
from datetime import timezone

from django.contrib.auth.models import User
from django.db import models


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    done_at = models.DateTimeField(null=True)
    deadline_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.title

    def __repr__(self):
        return '<Task object ({}) "{}">'.format(self.id, self.title)
