from django.urls import path

from favorites_app import views

urlpatterns = [
    path('', views.favorites_list, name='favorites_list'),
    path('toggle/<int:test_id>/', views.favorite_toggle, name='favorite_toggle'),
]