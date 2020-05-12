from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page, name='Login'),
]
