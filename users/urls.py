from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login, name='login'),
    path('signup/', views.sign_up, name='signup'),
path('logout/', views.logout, name='logout')
]