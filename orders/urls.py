from django.urls import path
from . import views

# path registrations below this line
app_name="orders"
urlpatterns = [
    path('daily_orders/', views.daily_orders, name="daily_orders.html"),
    path('add_orders/<int:client_id>/', views.add_order, name="add_order"),
]