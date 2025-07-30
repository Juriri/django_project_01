from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import Todo
from .forms import TodoForm, TodoUpdateForm


class TodoListView(LoginRequiredMixin, ListView):
    model = Todo
    template_name = 'todolist/todo_list.html'
    context_object_name = 'page_obj'
    paginate_by = 3

    def get_queryset(self):
        q = self.request.GET.get('q', '')
        qs = Todo.objects.filter(user=self.request.user)
        if q:
            qs = qs.filter(title__icontains=q)
        return qs.order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')
        return context


class TodoDetailView(LoginRequiredMixin, DetailView):
    model = Todo
    template_name = 'todolist/todo_info.html'
    context_object_name = 'todo'

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)


class TodoCreateView(LoginRequiredMixin, CreateView):
    model = Todo
    form_class = TodoForm
    template_name = 'todolist/todo_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('todo_info', kwargs={'todo_id': self.object.id})


class TodoUpdateView(LoginRequiredMixin, UpdateView):
    model = Todo
    form_class = TodoUpdateForm
    template_name = 'todolist/todo_update.html'

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('todo_info', kwargs={'todo_id': self.object.id})


class TodoDeleteView(LoginRequiredMixin, DeleteView):
    model = Todo
    template_name = 'todolist/todo_confirm_delete.html'
    success_url = reverse_lazy('todo_list')

    def get_queryset(self):
        return Todo.objects.filter(user=self.request.user)
