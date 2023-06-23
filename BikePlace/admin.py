from django.contrib import admin


from Acquista.models import *
from BikePlace.models import *

admin.site.register(GenericUser)
admin.site.register(Bike)
admin.site.register(ShoppingCart)
admin.site.register(ShoppingCartItem)
admin.site.register(BikeViewed)
admin.site.register(SoldBike)
admin.site.register(Order)
admin.site.register(Seller)
admin.site.register(FavoriteBike)
admin.site.register(Category)
admin.site.register(UserInterest)
admin.site.register(BikeComponent)
admin.site.register(CompositeBike)
