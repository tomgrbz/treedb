
from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create, name='create'),
    path('<int:tid>/view/', views.view, name='view'),
    #path('collection/', views.AllView.as_view(), name='allview'),
    path('register/', views.register, name='register'),
    path('collection/', views.collection, name='collection'),
    path('<int:tid>/delete/', views.delete_view, name='delete'),
    path('<int:ttid>/neighborhoods/', views.neighbor_view, name='neighborhoods'),
    
]

#views.view