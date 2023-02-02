from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name='index'),

    path("motociklai/", views.motociklai, name='motociklai'),
    path("motociklai/<int:motociklas_id>", views.motociklas, name='motociklas'),
    path("uzsakymai/", views.UzsakymasListView.as_view(), name='uzsakymai'),
    path("uzsakymai/<int:pk>", views.UzsakymasDetailView.as_view(), name='uzsakymas_detail'),
    path("paslaugos/", views.PaslaugaListView.as_view(), name='paslaugos'),
    path('search/', views.search, name='search'),
    path('register/', views.register, name='register'),
    path('profilis/', views.profilis, name='profilis'),
    path('manouzsakymai/', views.VartotojasListView.as_view(), name='manouzsakymai'),
    path('manouzsakymai/naujas', views.UzsakymasPagalVartotojasCreateView.as_view(), name='manouzsakymainaujas'),
    path('manouzsakymai/<int:pk>/update', views.UzsakymasPagalVartotojasUpdateView.as_view(), name='manouzsakymaiupdate'),
    path('manouzsakymai/<int:pk>/delete', views.UzsakymasPagalVartotojasDeleteView.as_view(), name='manouzsakymaidelete'),
    path('manouzsakymai/<int:pk2>/eiluteedit/<int:pk>', views.PaslaugosRedagavimasUpdateView.as_view(), name='paslaugosredagavimas'),
    path('manouzsakymai/<int:pk2>/eilutedelete/<int:pk>', views.PaslaugosTrinimoView.as_view(), name='paslaugostrinimas'),
    path('uzsakymai/<int:pk>/prideti', views.PaslaugaPridetiCreateView.as_view(), name='paslaugospridejimas'),

]