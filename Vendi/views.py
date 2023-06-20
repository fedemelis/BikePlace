from django.shortcuts import render
from braces.views import *
from django.urls import reverse_lazy
from django.views.generic import *

from Acquista.models import Bike


class BikeOnSale(LoginRequiredMixin, ListView):
    model = Bike
    template_name = 'bike_on_sale.html'
    context_object_name = 'bici_in_vendita'

    def get_queryset(self):
        user_id = self.request.user.pk
        return Bike.objects.filter(vendor=user_id)


class BikeUpdateView(LoginRequiredMixin, UpdateView):
    model = Bike
    fields = ['type_of_bike', 'brand', 'year_of_production', 'price', 'image']
    template_name = 'bike_update.html'
    success_url = reverse_lazy('Vendi:home_vendite')

class BikeCreateView(LoginRequiredMixin, CreateView):
    model = Bike
    fields = ['type_of_bike', 'brand', 'year_of_production', 'price', 'image']
    template_name = 'add_bike.html'
    success_url = reverse_lazy('Vendi:home_vendite')

    def form_valid(self, form):
        form.instance.vendor = self.request.user
        return super().form_valid(form)
