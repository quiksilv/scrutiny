from django.urls import path
from . import views

urlpatterns = [
    path('thestar/', views.thestar, name='thestar'),
]

