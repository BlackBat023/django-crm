from django.urls import path
from . import views

# path registrations below this line
app_name="orders"
urlpatterns = [
    path('create/<int:client_id>/', views.order_create, name='order_create'),
    path('<pk>/', views.order_detail, name='order_detail'),
    path('<pk>/item/create/', views.order_item_create, name='order_item_create'),
    path('update/<int:pk>/', views.order_update, name='order_update'),
    path('delete/<int:pk>/', views.order_delete, name='order_delete'),
    path('', views.order_list, name='order_list.html'),
]