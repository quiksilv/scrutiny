from django.urls import path
from . import views

urlpatterns = [
    path('aggregator/', views.aggregator, name='aggregator'),
    path('scrap/', views.scrap, name='scrap'),
]

