from django.urls import path
from . import views

urlpatterns = [
	path('', views.store, name="store"),
	# path('filterProducts/', views.filterProducts, name="filter"),
	path('trainings/', views.trainings, name="trainings"),
	path('diets/', views.diets, name="diets"),
	path('about/', views.about, name="about"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('cart/update_item/', views.updateItem, name="update_item"),
	path('process_order/',views.processOrder, name="process_order"),
]