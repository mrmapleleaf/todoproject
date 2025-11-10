from django.urls import path
from . import views

urlpatterns = [
    path("", views.todo_list, name="todo_list"),
    path("add/", views.todo_create, name="todo_create"),
    path("delete/<int:todo_id>/", views.todo_delete, name="todo_delete"),
    path(
        "update_status/<int:todo_id>/",
        views.todo_update_status,
        name="todo_update_status",
    ),
    path("edit/<int:todo_id>/", views.todo_edit, name="todo_edit"),
    path("detail/<int:todo_id>/", views.todo_detail, name="todo_detail"),
]
