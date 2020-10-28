from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('view/<str:name>', views.view, name='view'),
]
