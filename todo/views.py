from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import ToDoItem
from .forms import ToDoItemForm


# Create your views here.
def todo_list(request):
    todos = ToDoItem.objects.all().order_by("-created_at")
    return render(request, "todo/todo_list.html", {"todos": todos})


def todo_detail(request, todo_id):
    todo = get_object_or_404(ToDoItem, id=todo_id)
    return render(request, "todo/todo_detail.html", {"todo": todo})


def todo_create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        if title:
            ToDoItem.objects.create(title=title)
            return redirect("todo_list")
    return render(request, "todo/todo_form.html")


def todo_edit(request, todo_id):
    todo = get_object_or_404(ToDoItem, id=todo_id)

    # POSTリクエストの場合は、フォームの内容を更新して保存する
    if request.method == "POST":
        form = ToDoItemForm(request.POST, instance=todo)
        if form.is_valid():
            form.save()
            return redirect("todo_list")
    else:
        form = ToDoItemForm(instance=todo)
    return render(request, "todo/todo_edit.html", {"form": form})


def todo_delete(request, todo_id):
    todo = get_object_or_404(ToDoItem, id=todo_id)
    todo.delete()
    return redirect("todo_list")


@require_POST
def todo_update_status(request, todo_id):
    # todo = ToDoItem.objects.get(id=todo_id)
    todo = get_object_or_404(ToDoItem, id=todo_id)
    todo.is_completed = not todo.is_completed
    todo.save()
    return redirect("todo_list")
