from django.urls import path
from . import views

urlpatterns = [
    path('mentions/<int:p_id>/', views.mentions, name='mentions'),
]

