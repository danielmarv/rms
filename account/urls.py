from django.urls import path
from . import views

urlpatterns = [
    path('', views.account_login, name="account_login"),
    path('register/', views.account_register, name="account_register"),
    path('dep/', views.create_department, name="create_department"),
    path('logout/', views.account_logout, name="account_logout"),
    path('lock/', views.lock, name='register'),
]
