from django.db import models
from django.contrib.auth.models import User


class ToDoItem(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        # ユーザーからToDoItemを逆参照する際の属性名
        related_name="todos",
        null=True,
    )
    due_date = models.DateField(null=True, blank=True)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} ： {self.title} ({self.user.username})"
