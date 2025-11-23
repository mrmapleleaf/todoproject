from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import Http404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from .models import ToDoItem, models
from .forms import ToDoItemForm
from datetime import date


@login_required
def todo_list(request):

    # 最初にユーザーに紐づくToDoItemを取得
    todos = ToDoItem.objects.filter(user=request.user)

    # クエリパラメータからステータスを取得
    status = request.GET.get("status")
    if status == "done":
        todos = todos.filter(is_completed=True)
    elif status == "undone":
        todos = todos.filter(is_completed=False)
    elif status == "all" or status is None:
        pass
    else:
        raise Http404("不正なステータスです。")

    # クエリパラメータからソート条件を取得
    sort_param = request.GET.get("sort", "created_at_desc")
    # order_byの引数に「-」があると降順、ないと昇順
    # デフォルトは作成日の降順
    if sort_param == "due_date_asc":
        ordering = [
            models.Case(
                models.When(due_date__isnull=True, then=models.Value(0)),
                default=models.Value(1),
                output_field=models.IntegerField(),
            ),
            "due_date",
        ]
    elif sort_param == "due_date_desc":
        # due_dateがnullのものは先頭に持ってくる
        ordering = [
            models.Case(
                models.When(due_date__isnull=True, then=models.Value(0)),
                default=models.Value(1),
                output_field=models.IntegerField(),
            ),
            "-due_date",
        ]
    elif sort_param == "created_at_asc":
        ordering = ["created_at"]
    elif sort_param == "created_at_desc" or not sort_param:
        ordering = ["-created_at"]
    else:
        raise Http404("不正なソート条件です。")

    todos = todos.order_by(*ordering)

    return render(
        request,
        "todo/todo_list.html",
        {"todos": todos, "status": status, "today": date.today(), "sort": sort_param},
    )


@login_required
def todo_detail(request, todo_id):
    todo = get_object_or_404(ToDoItem, id=todo_id, user=request.user)
    return render(request, "todo/todo_detail.html", {"todo": todo})


@login_required
def todo_create(request):
    if request.method == "POST":
        form = ToDoItemForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()
            return redirect("todo_list")
    else:
        form = ToDoItemForm()
    return render(request, "todo/todo_form.html", {"form": form})


@login_required
def todo_edit(request, todo_id):
    todo = get_object_or_404(ToDoItem, id=todo_id, user=request.user)

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
    todo = get_object_or_404(ToDoItem, id=todo_id, user=request.user)
    todo.delete()
    return redirect("todo_list")


@login_required
@require_POST
def todo_update_status(request, todo_id):
    # todo = ToDoItem.objects.get(id=todo_id)
    todo = get_object_or_404(ToDoItem, id=todo_id, user=request.user)
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
