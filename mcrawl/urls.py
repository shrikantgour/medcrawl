from django.contrib import admin
from django.urls import path
from . import views


urlpatterns = [
    path("", views.index ,name='mcrawl'),
    path('tagger/', views.tagger,name = 'ntag')
]

