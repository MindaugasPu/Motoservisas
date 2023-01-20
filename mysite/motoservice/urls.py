from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("motociklai/", views.motociklai, name='motociklai'),
    path("motociklai/<int:motociklas_id>", views.motociklas, name='motociklas'),
    path("paslaugos/", views.PaslaugaListView.as_view(), name='paslaugos'),
]