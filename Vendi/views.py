from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from braces.views import *
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import *

from Acquista.models import Bike


class BikeOnSale(LoginRequiredMixin, ListView):
    model = Bike
    template_name = 'bike_on_sale.html'
    context_object_name = 'bici_in_vendita'
    paginate_by = 6

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

@require_POST
def delete_bike(request, pk):
    bike = get_object_or_404(Bike, pk=pk)
    if not Bike.objects.contains(bike):
        return HttpResponse(status=407, content='Errore')
    bike.delete()
    return HttpResponse(status=207)