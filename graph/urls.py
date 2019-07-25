from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('face/new/', views.FaceView.as_view()),
    path('<str:face>/', views.detail, name='detail'),
    path('<str:face>/<str:emotion>/', views.detail_emotion, name='detail_emotion'),
]
