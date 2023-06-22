import os
import uuid

import piexif
from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from PIL import Image
from io import BytesIO


class GenericUser(AbstractUser):
    address = models.CharField(null=True, blank=True, max_length=100, verbose_name='indirizzo')
    picture = models.ImageField(blank=True, verbose_name='foto profilo', upload_to='profile_pics')
    piva = models.CharField(null=True, blank=True, max_length=11, verbose_name='partita iva')

    #TODO: gestire la dimensione dell'immagine


class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name='nome')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Categorie"


class UserInterest(models.Model):
    user = models.ForeignKey(GenericUser, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)

    def __str__(self):
        return f"{self.user.username} è interessato a {self.category.name}"

    class Meta:
        verbose_name_plural = "Interessi Utenti"