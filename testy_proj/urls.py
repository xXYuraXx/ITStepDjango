from django.contrib import admin
from django.urls import path
from tests_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.tests_list),
]
