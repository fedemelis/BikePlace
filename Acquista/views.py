from django.shortcuts import render
from django.views.generic import *

from Acquista.models import *


class BikeListView(ListView):
    model = Bike
    template_name = "listabike.html"
    context_object_name = "bici_list"

class BikeDetailView(DetailView):
    model = Bike
    template_name = "bikedetail.html"
    context_object_name = "bici"


