from django.urls import path
from tests_app import views

urlpatterns = [
    path('', views.tests_list, name="tests_list"),
    path('about/', views.about, name="about"),
    path('tests/admin/', views.admin_list, name="admin"),
    path('test/<int:test_id>/', views.test_detail, name='test_detail'),
    path('test/delete/<int:test_id>/', views.test_delete, name="test_delete"),
    path('test/create/', views.test_create, name='test_create'),
    path('test/edit/<int:test_id>/', views.test_edit, name="test_edit"),
    path('test/edit/<int:test_id>/<path:return_url>/', views.test_edit, name="test_edit_return"),
    path('test/search_by_id', views.search_by_id, name="search_by_id"),
    path('test/<int:test_id>/<int:question_order>/', views.test_question, name='test_question'),
    
]


