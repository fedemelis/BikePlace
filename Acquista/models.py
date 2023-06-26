from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone

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


class BikeComponent(models.Model):
    TYPE_OF_COMPONENT = [
        ('Telaio', 'Telaio'),
        ('Manubrio', 'Manubrio'),
        ('Freno', 'Freno'),
        ('Sellino', 'Sellino'),
        ('Copertoni', 'Copertoni')
    ]
    name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, choices=TYPE_OF_COMPONENT)
    price = models.IntegerField()
    vendor = models.ForeignKey(GenericUser, on_delete=models.CASCADE, related_name='component_vendor')

    class Meta:
        verbose_name_plural = "Componenti Bici"

    def __str__(self):
        return self.name


class CompositeBike(Bike):
    telaio = models.ForeignKey(BikeComponent, on_delete=models.CASCADE, related_name='composite_telaio')
    manubrio = models.ForeignKey(BikeComponent, on_delete=models.CASCADE, related_name='composite_manubrio')
    freno = models.ForeignKey(BikeComponent, on_delete=models.CASCADE, related_name='composite_freno')
    sellino = models.ForeignKey(BikeComponent, on_delete=models.CASCADE, related_name='composite_sellino')
    copertoni = models.ForeignKey(BikeComponent, on_delete=models.CASCADE, related_name='composite_copertoni')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.type_of_bike = 'Bici Composte'
        self.brand = 'Creata da me'
        self.year_of_production = timezone.now().year
        # self.vendor = None
        # self.image = None

    def save(
        self, force_insert=False, force_update=False, using=None, update_fields=None
    ):
        self.price = self.telaio.price + self.manubrio.price + self.freno.price + self.sellino.price + self.copertoni.price
        super().save(force_insert, force_update, using, update_fields)

    class Meta:
        verbose_name_plural = "Bici Composte"


class BikeDiscount(models.Model):
    user = models.ForeignKey(GenericUser, on_delete=models.CASCADE, related_name='discount')
    bike = models.ForeignKey(Bike, on_delete=models.CASCADE, related_name='discount')
    newPrice = models.IntegerField()
    start_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Sconto sulla bici {self.bike.type_of_bike} {self.bike.brand}"

    class Meta:
        verbose_name_plural = "Sconti Bici"

