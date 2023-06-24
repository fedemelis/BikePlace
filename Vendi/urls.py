from . import views
from .views import *
from django.urls import path

app_name = 'Vendi'

urlpatterns = [

    path('', views.BikeOnSale.as_view(), name='home_vendite'),

    path('updatebike/<pk>/', views.BikeUpdateView.as_view(), name='bike_update'),
    path('addbike/', views.BikeCreateView.as_view(), name='add_bike'),
    path('deletebike/<pk>/', delete_bike, name='delete_bike'),

    path('homevendor/', views.HomeVendorView.as_view(), name='home_vendor'),
    path('usersfavorite/', views.UsersFavoriteView.as_view(), name='users_favorite'),

    path('addcomponent', views.AddComponentView.as_view(), name='add_component'),
    path('listcomponents/', views.ComponentListView.as_view(), name='list_components'),
    path('deletecomponent/<pk>/', views.delete_component, name='delete_component'),
    path('updatecomponent/<pk>/', views.ComponentUpdateView.as_view(), name='update_component'),

]