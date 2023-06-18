from . import views
from django.urls import path

app_name = 'Acquista'

urlpatterns = [

    path('listabici/', views.BikeListView.as_view(), name='listabici'),
    path('dettagliobici/<pk>/', views.BikeDetailView.as_view(), name='dettagliobici'),

]
