from django.urls import path
from .views import menu_home_page

urlpatterns = [
    path("menu/", menu_home_page, name="home")
]