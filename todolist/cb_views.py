from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import TodoForm
from .models import Todo


class TodoListView(LoginRequiredMixin, ListView):
    model = Todo
    template_name = 'todolist/todo_list.html'
    page_obj = 'page_obj'
    paginate_by = 3

    def get_queryset(self):
        q = self.request.GET.get('q', '')
        qs = Todo.objects.filter(user=self.request.user)
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(description__icontains=q))
        return qs.order_by('-id')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['q'] = self.request.GET.get('q', '')

        return context


class TodoDetailView(LoginRequiredMixin, DetailView):
    model = Todo
    template_name = 'todolist/todo_info.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.user != self.request.user and not self.request.user.is_superuser:
            raise Http404("해당 To Do를 조회할 권한이 없습니다.")
        return obj

    def get_context_data(self, **kwargs):
        context = {'todo': self.object.__dict__}
        return context


class TodoCreateView(LoginRequiredMixin, CreateView):
    model = Todo
    form_class = TodoForm
    template_name = 'todolist/todo_create.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("cbv_todo_info", kwargs={"pk": self.object.id})


class TodoUpdateView(LoginRequiredMixin, UpdateView):
    model = Todo
    fields = ['title', 'description', 'start_date', 'end_date', 'is_completed', 'id']
    template_name = 'todolist/todo_update.html'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.user != self.request.user and not self.request.user.is_superuser:
            raise Http404("해당 To Do를 수정할 권한이 없습니다.")
        return obj

    def get_success_url(self):
        return reverse_lazy('cbv_todo_info', kwargs={'pk': self.object.id})

class TodoDeleteView(LoginRequiredMixin, DeleteView):
    model = Todo

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)

        if obj.user != self.request.user and not self.request.user.is_superuser:
            raise Http404("해당 To Do를 삭제할 권한이 없습니다.")
        return obj

    def get_success_url(self):
        return reverse_lazy('cbv_todo_list')
