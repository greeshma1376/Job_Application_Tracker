from django.db import models

class Task(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    due_date = models.DateField()
    is_completed = models.BooleanField(default=False)

    class Meta:
        ordering = ['due_date', '-id']

    def __str__(self):
        return self.title
