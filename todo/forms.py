from django import forms
from .models import ToDoItem
from datetime import date
from django.core.exceptions import ValidationError


# 新規作成、編集用のフォームクラス。modelとは分けて作る方がそれぞれの責務を明確にできるので望ましい。
class ToDoItemForm(forms.ModelForm):
    due_date = forms.DateField(
        required=False, widget=forms.DateInput(attrs={"type": "date"})
    )

    class Meta:
        model = ToDoItem
        fields = ["title", "due_date", "is_completed"]

    # clean_xxxのバリデーションメソッドを定義すると、xxxのフィールドに対して、独自バリデーションを追加できる
    def clean_due_date(self):
        due = self.cleaned_data.get("due_date")
        if due and due < date.today():
            raise ValidationError("過去日の指定はできません。")
        return due
