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
