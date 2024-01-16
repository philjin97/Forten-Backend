from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.UserRegister.as_view()),
    path('login/', views.UserLogin.as_view()),
    path('logout/', views.UserLogout.as_view()),
    path('memo/', views.MemoUpdate.as_view()),
    path('favorite/<int:user_id>/<int:student_id>/', views.FavoriteAPIView.as_view()),
    path('favorite/<int:user_id>/', views.FavoriteGetAPIView.as_view())
]