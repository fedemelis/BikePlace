from . import views
from django.urls import path

app_name = 'Acquista'

urlpatterns = [

    path('', views.HomeAcquistiView.as_view, name='home_acquisti'),

    path('listabici/', views.BikeListView.as_view(), name='listabici'),
    path('dettagliobici/<pk>/', views.BikeDetailView.as_view(), name='dettagliobici'),

    path('homeacquisti/', views.HomeAcquistiView.as_view(), name='home_acquisti'),

    path('carrello/<str:status>/', views.ShoppingCartView.as_view(), name='carrello'),
    path('aggiungi-al-carrello/<pk>/', views.AggiungiAlCarrelloView.as_view(), name='aggiungi-al-carrello'),
    path('rimuovi-dal-carrello/<pk>/', views.RimuoviDalCarrelloView.as_view(), name='rimuovi-dal-carrello'),
    path('svuota-carrello/<pk>/', views.flush_shopping_cart, name='svuota-carrello'),
    path('ordine_confermato/<pk>/', views.OrderConfirmationView.as_view(), name='ordine_confermato'),

    path('ordini/', views.OrderListView.as_view(), name='ordini'),

    path('rimuovi-preferito/<pk>/', views.RimuoviPreferitoView.as_view(), name='rimuovi-preferito'),
    path('rimuovi-da-lista-preferiti/<pk>/', views.RimuoviPreferitoFromList.as_view(), name='rimuovi-da-lista-preferiti'),
    path('aggiungi-preferito/<pk>/', views.AggiungiPreferitoView.as_view(), name='aggiungi-preferito'),


    path('listapreferiti/<pk>/', views.FavoriteBikeListView.as_view(), name='listapreferiti'),

]
