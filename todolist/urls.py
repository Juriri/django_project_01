from django.urls import path

from . import cb_views

urlpatterns = [
    path('', cb_views.TodoListView.as_view(), name='cbv_todo_list'),
    path('<int:pk>/', cb_views.TodoDetailView.as_view(), name='cbv_todo_info'),
    path('create/', cb_views.TodoCreateView.as_view(), name='cbv_todo_create'),
    path('<int:pk>/update/', cb_views.TodoUpdateView.as_view(), name='cbv_todo_update'),
    path('<int:pk>/delete/', cb_views.TodoDeleteView.as_view(), name='cbv_todo_delete'),
    path('comment/<int:todo_id>/create/', cb_views.CommentCreateView.as_view(), name='cbv_comment_create'),
    path('comment/<int:pk>/update/', cb_views.CommentUpdateView.as_view(), name='cbv_comment_update'),
    path('comment/<int:pk>/delete/', cb_views.CommentDeleteView.as_view(), name='cbv_comment_delete'),
]
