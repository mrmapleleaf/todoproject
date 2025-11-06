from django.db import models


class ToDoItem(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} ： {self.title}"
