from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="hello"),
    path("<str:name>", views.greet, name="hello")
]