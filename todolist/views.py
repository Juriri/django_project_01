from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from .forms import TodoForm, TodoUpdateForm
from .models import Todo


@login_required
def todo_list(request):
    q = request.GET.get("q", "")
    todo_all = Todo.objects.filter(user=request.user)

    if q:
        todo_all = todo_all.filter(Q(title__icontains=q) | Q(description__icontains=q))

    paginator = Paginator(todo_all, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    context = {"page_obj": page_obj, "q": q}
    return render(request, "todolist/todo_list.html", context)


@login_required
def todo_info(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    context = {"todo": todo.__dict__}
    return render(request, "todolist/todo_info.html", context)


@login_required
def todo_create(request):
    form = TodoForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        todo = form.save(commit=False)
        todo.user = request.user
        todo.save()
        return redirect("todolist/todo_info", todo_id=todo.id)
    return render(request, "todolist/todo_create.html", {"form": form})


@login_required()
def todo_update(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    form = TodoUpdateForm(request.Post or None, instance=todo)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("todo_info", todo_id=todo_id)
    return render(request, "todolist/todo_update.html", {"form": form})


@login_required()
def todo_delete(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id, user=request.user)
    if request.method == "POST":
        todo.delete()
        return redirect("todo_list")
    return render(request, "todolist/todo_list.html", {"todo": todo})
