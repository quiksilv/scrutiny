from django.urls import path
from . import views

urlpatterns = [
    path('view/<str:name>', views.view, name='view'),
]
