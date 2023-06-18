from . import views
from django.urls import path

app_name = 'Vendita'

urlpatterns = [

    path('listabici/', views.BikeListView.as_view(), name='vendita'),

]
