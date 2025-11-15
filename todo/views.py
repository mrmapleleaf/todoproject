from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .models import ToDoItem
from .forms import ToDoItemForm
from django.http import Http404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required


@login_required
def todo_list(request):
    status = request.GET.get("status")
    todos = ToDoItem.objects.order_by("-id")

    if status == "done":
        todos = todos.filter(is_completed=True)
    elif status == "undone":
        todos = todos.filter(is_completed=False)
    elif status == "all" or status is None:
        pass
    else:
        raise Http404("不正なステータスです。")

    return render(request, "todo/todo_list.html", {"todos": todos, "status": status})


@login_required
def todo_detail(request, todo_id):
    todo = get_object_or_404(ToDoItem, id=todo_id)
    return render(request, "todo/todo_detail.html", {"todo": todo})


@login_required
def todo_create(request):
    if request.method == "POST":
        title = request.POST.get("title")
        if title:
            ToDoItem.objects.create(title=title)
            return redirect("todo_list")
    return render(request, "todo/todo_form.html")


@login_required
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


@login_required
def todo_delete(request, todo_id):
    todo = get_object_or_404(ToDoItem, id=todo_id)
    todo.delete()
    return redirect("todo_list")


@login_required
@require_POST
def todo_update_status(request, todo_id):
    # todo = ToDoItem.objects.get(id=todo_id)
    todo = get_object_or_404(ToDoItem, id=todo_id)
    todo.is_completed = not todo.is_completed
    todo.save()
    return redirect("todo_list")


def sign_up(request):
    if request.method == "POST":
        # POSTの時はフォームの内容を処理して、ユーザー作成
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("todo_list")
    else:
        # GETの時は空のフォーム表示
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})
