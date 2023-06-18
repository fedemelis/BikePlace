from django.shortcuts import render
from django.views.generic import *

from Vendita.models import *


class BikeListView(ListView):
    model = Bike
    template_name = "listabike.html"
    context_object_name = "bici_list"
