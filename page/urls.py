from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='page-home'),
    path('<str:params>', views.search, name='page-search'),
    path('view/<str:params>', views.view, name='page-view')
]