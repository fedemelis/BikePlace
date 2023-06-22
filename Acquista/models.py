from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from BikePlace.models import GenericUser


class Bike(models.Model):
    TYPE_OF_BIKE = [
        ('Bici da strada', 'Bici da Strada'),
        ('Bici da montagna', 'Bici da Montagna'),
        ('Bici da città', 'Bici da Città'),
        ('Bici ibride', 'Bici Ibride'),
        ('Bici da corsa', 'Bici da Corsa'),
        ('Bici da cicloturismo', 'Bici da Cicloturismo'),
        ('Bici da gravel', 'Bici da Gravel'),
        ('Bici da pista', 'Bici da Pista'),
        ('Bici BMX', 'Bici BMX'),
        ('Bici pieghevoli', 'Bici Pieghevoli'),
    ]
    type_of_bike = models.CharField(max_length=20, choices=TYPE_OF_BIKE)
    brand = models.CharField(max_length=50)
    year_of_production = models.IntegerField()
    price = models.IntegerField()
    vendor = models.ForeignKey(GenericUser, on_delete=models.CASCADE, related_name='venditore')
    image = models.ImageField(upload_to='bici_images')

    def __str__(self):
        out = "Tipo di bici: {}<br>".format(self.type_of_bike)
        out += "Marca: {}<br>".format(self.brand)
        out += "Anno di produzione: {}<br>".format(self.year_of_production)
        out += "Prezzo: {}<br>".format(self.price)
        out += "Venditore: {}<br>".format(self.vendor.username)
        return out

    class Meta:
        verbose_name_plural = "Bici"


class ShoppingCart(models.Model):
    user = models.OneToOneField(GenericUser, on_delete=models.CASCADE, related_name='shopping_cart')

    def __str__(self):
        return f"Carrello utente: {self.user.username}"


class ShoppingCartItem(models.Model):
    shopping_cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE, related_name='items')
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE, related_name='cart_items')

    def __str__(self):
        return f"Bici nel carrello di {self.shopping_cart.user.username}: {self.bike.type_of_bike} {self.bike.brand}"


@receiver(post_save, sender=GenericUser)
def create_shopping_cart(sender, instance, created, **kwargs):
    if created:
        ShoppingCart.objects.create(user=instance)


class BikeViewed(models.Model):
    user = models.ForeignKey(GenericUser, on_delete=models.CASCADE)
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Bici Viste"


class SoldBike(Bike):
    class Meta:
        verbose_name_plural = "Bici Vendute"


class Seller(GenericUser):
    class Meta:
        verbose_name_plural = "Venditori"


class Order(models.Model):
    user = models.ForeignKey(GenericUser, on_delete=models.CASCADE, related_name='orders')
    sold_bikes = models.ManyToManyField(SoldBike, related_name='orders')
    order_date = models.DateTimeField(auto_now_add=True)
    total_price = models.IntegerField()

    def __str__(self):
        return f"Ordine di {self.user.username}"

    class Meta:
        verbose_name_plural = "Ordini"


class FavoriteBike(models.Model):
    user = models.ForeignKey(GenericUser, on_delete=models.CASCADE, related_name='favorites')
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE, related_name='favorites')
    viewed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bici preferita di {self.user.username}: {self.bike.type_of_bike} {self.bike.brand}"

    class Meta:
        verbose_name_plural = "Preferiti"
        unique_together = ['user', 'bike']

