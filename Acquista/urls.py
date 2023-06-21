from . import views
from django.urls import path

app_name = 'Acquista'

urlpatterns = [

    path('', views.HomeAcquistiView.as_view, name='home_acquisti'),

    path('listabici/', views.BikeListView.as_view(), name='listabici'),
    path('dettagliobici/<pk>/', views.BikeDetailView.as_view(), name='dettagliobici'),

    path('homeacquisti/', views.HomeAcquistiView.as_view(), name='home_acquisti'),

    path('carrello/', views.ShoppingCartView.as_view(), name='carrello'),
    path('aggiungi-al-carrello/<pk>/', views.AggiungiAlCarrelloView.as_view(), name='aggiungi-al-carrello'),
    path('rimuovi-dal-carrello/<pk>/', views.RimuoviDalCarrelloView.as_view(), name='rimuovi-dal-carrello'),

]
