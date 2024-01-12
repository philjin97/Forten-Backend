from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.UserRegister.as_view()),
    path('login/', views.UserLogin.as_view()),
    path('logout/', views.UserLogout.as_view()),
    
]