from django.urls import path
from . import views

urlpatterns = [
    path('process/', views.process, name='process'),
    path('view/<str:name>', views.view, name='view'),
]
