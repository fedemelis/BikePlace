from django.db import models

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
    image = models.ImageField(default=None, blank=True ,upload_to='bici_images')

    def __str__(self):
        out = "Tipo di bici:" + self.type_of_bike + " marca:" + self.brand + " anno di produzione:" + str(
            self.year_of_production) + " prezzo:" + str(self.price) + " venditore:" + self.vendor.username
        return out

    class Meta:
        verbose_name_plural = "Bici"
