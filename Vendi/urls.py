from . import views
from .views import *
from django.urls import path

app_name = 'Vendi'

urlpatterns = [

    path('', views.BikeOnSale.as_view(), name='home_vendite'),

    path('updatebike/<pk>/', views.BikeUpdateView.as_view(), name='bike_update'),
    path('addbike/', views.BikeCreateView.as_view(), name='add_bike'),
    path('deletebike/<pk>/', delete_bike, name='delete_bike'),

]