from django.contrib import admin


from Acquista.models import *

admin.site.register(GenericUser)
admin.site.register(Bike)
admin.site.register(ShoppingCart)
admin.site.register(ShoppingCartItem)
admin.site.register(BikeViewed)
