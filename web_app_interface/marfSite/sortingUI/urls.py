from django.urls import path
from . import views

urlpatterns = [
    path('', views.index.as_view(), name='sorting'),
    path('user/<slug:userId>/', views.userPage, name='userPage'),
    path('set/<slug:setName>/', views.setPage, name='setPage')
]
