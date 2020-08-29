from django.urls import path
from tokens import views

urlpatterns = [
    path('', views.index, name='index'),
]
