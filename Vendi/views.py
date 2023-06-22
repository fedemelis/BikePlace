from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from braces.views import *
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import *
from PIL import Image

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

    def form_valid(self, form):
        # Validazione dell'anno di produzione
        year = form.cleaned_data['year_of_production']
        if year < 1900 or year > 2023:
            form.add_error('year_of_production', 'L\'anno di produzione deve essere compreso tra 1900 e 2023.')
            return self.form_invalid(form)

        return super().form_valid(form)




class BikeCreateView(LoginRequiredMixin, CreateView):
    model = Bike
    fields = ['type_of_bike', 'brand', 'year_of_production', 'price', 'image']
    template_name = 'add_bike.html'
    success_url = reverse_lazy('Vendi:home_vendite')

    # def form_valid(self, form):
    #     form.instance.vendor = self.request.user
    #     return super().form_valid(form)

    def form_valid(self, form):
        form.instance.vendor = self.request.user

        # Ottieni l'istanza del modulo Bike
        bike = form.save(commit=False)

        # Ridimensiona l'immagine
        image = form.cleaned_data['image']
        max_image_size = (400, 300)  # Dimensioni massime dell'immagine desiderate
        try:
            img = Image.open(image)
            img.thumbnail(max_image_size, Image.ANTIALIAS)
            img.save(bike.image.path)
        except IOError:
            # Gestisci l'errore se l'immagine non può essere ridimensionata
            form.add_error('image',
                           'Impossibile ridimensionare l\'immagine. Assicurati che sia nel formato corretto e abbia dimensioni adeguate.')

        year = form.cleaned_data['year_of_production']
        if year < 1900 or year > 2023:
            form.add_error('year_of_production', 'L\'anno di produzione deve essere compreso tra 1900 e 2023.')
            return self.form_invalid(form)

        bike.save()

        return super().form_valid(form)



@require_POST
def delete_bike(request, pk):
    bike = get_object_or_404(Bike, pk=pk)
    if not Bike.objects.contains(bike):
        return HttpResponse(status=407, content='Errore')
    bike.delete()
    return HttpResponse(status=207)