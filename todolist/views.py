from django.shortcuts import get_object_or_404
from .models import Todo
from django.template.response import TemplateResponse

def todo_list(request):
    todos = Todo.objects.all()
    return TemplateResponse(request, 'todolist/todo_list.jinja.html', {'todos': todos})

def todo_info(request, todo_id):
    todo = get_object_or_404(Todo, id=todo_id)
    return TemplateResponse(request, 'todolist/todo_info.jinja.html', {'todo': todo})
