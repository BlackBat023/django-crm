from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home.html"),
    # path('login/', views.login_user, name="login.html"),
    path('logout/', views.logout_user, name="logout.html"),
    path('register/', views.register_user, name="register.html"),
    path('client_details/<int:pk>', views.client_details, name="client_details.html"),
    path('delete_details/<int:pk>', views.delete_details, name="delete_details"),
    path('add_client/', views.add_client, name="add_client.html"),
    path('edit_details/<int:pk>', views.edit_details, name="edit_details.html"),
    path('filter/', views.filter, name="filter")
]