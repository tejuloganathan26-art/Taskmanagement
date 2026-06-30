from django.db import models
from projects.models import Project

class Task(models.Model):

    project = models.ForeignKey(Project,on_delete=models.CASCADE)

    title = models.CharField(max_length=200)

    description = models.TextField()

    priority = models.CharField(max_length=20)

    status = models.CharField(max_length=20)

    due_date = models.DateField()

    def __str__(self):
        return self.title
