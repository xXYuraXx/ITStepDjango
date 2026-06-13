from django.urls import path
from tests_app import views

urlpatterns = [
    path('', views.tests_list, name="tests_list"),
    path('about/', views.about, name="about"),
    path('test/<int:test_id>/', views.test_detail, name='test_detail'),
]


