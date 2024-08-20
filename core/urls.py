from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home.html"),
    # path('login/', views.login_user, name="login.html"),
    path('logout/', views.logout_user, name="logout.html"),
    path('register/', views.register_user, name="register.html"),
]