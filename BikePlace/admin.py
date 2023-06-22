from django.contrib import admin


from Acquista.models import *

admin.site.register(GenericUser)
admin.site.register(Bike)
admin.site.register(ShoppingCart)
admin.site.register(ShoppingCartItem)
admin.site.register(BikeViewed)
admin.site.register(SoldBike)
admin.site.register(Order)
admin.site.register(Seller)
admin.site.register(FavoriteBike)
