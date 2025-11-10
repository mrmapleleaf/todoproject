from django import forms
from .models import ToDoItem


# 新規作成、編集用のフォームクラス。modelとは分けて作る方がそれぞれの責務を明確にできるので望ましい。
class ToDoItemForm(forms.ModelForm):
    class Meta:
        model = ToDoItem
        fields = ["title", "is_completed"]
