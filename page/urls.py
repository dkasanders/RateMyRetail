from django.urls import path
from . import views
from django.contrib import admin

urlpatterns = [
    path('', views.home, name='page-home'),
    path('<str:params>', views.search, name='page-search'),
    path('view/<str:params>', views.view, name='page-view'),
    path('review/<str:id>', views.review, name='page-review'),

]