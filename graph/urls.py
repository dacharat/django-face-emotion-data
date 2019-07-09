from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<str:face>/', views.detail, name='detail'),
]
