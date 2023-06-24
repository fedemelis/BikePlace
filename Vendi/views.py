from django.core.exceptions import ValidationError
from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from braces.views import *
from django.urls import reverse_lazy
from django.views.decorators.http import require_POST
from django.views.generic import *
from PIL import Image

from Acquista.models import Bike, BikeComponent


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


class HomeVendorView(GroupRequiredMixin, TemplateView):
    group_required = "Vendors"
    template_name = 'home_vendor.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Ottieni le 3 bici più popolari tra i preferiti degli utenti usando la foreign key inversa favorites che si riferisce a Bike
        popular_bikes = Bike.objects.annotate(num_favorites=Count('favorites')).order_by('-num_favorites')[:3]

        # Aggiungi le bici al contesto
        context['popular_bikes'] = popular_bikes

        return context


class UsersFavoriteView(GroupRequiredMixin, ListView):
    group_required = "Vendors"
    model = Bike
    template_name = 'users_favorite.html'
    paginate_by = 6

    def get_queryset(self):
        # Ottieni l'ID del venditore attuale
        vendor_id = self.request.user.id

        # Ottieni tutte le bici in vendita del venditore escludendo le bici vendute
        bikes_for_sale = Bike.objects.filter(vendor_id=vendor_id).exclude(soldbike__isnull=False)

        # Ottieni le bici popolari tra i preferiti degli utenti
        popular_bikes = bikes_for_sale.annotate(num_favorites=Count('favorites')).order_by('-num_favorites')

        return popular_bikes


class AddComponentView(GroupRequiredMixin, CreateView):
    group_required = "Vendors"
    model = BikeComponent
    fields = ['category', 'name', 'price']
    template_name = 'add_component.html'
    success_url = reverse_lazy('Vendi:home_vendor')
    # differenziare i success url

    def get_success_url(self):
        referer = self.request.GET.get('next')
        if referer:
            if 'homevendor' in referer:
                return reverse_lazy('Vendi:home_vendor')
            elif 'listcomponents' in referer:
                return reverse_lazy('Vendi:list_components')
        return self.success_url

    def form_valid(self, form):
        form.instance.vendor = self.request.user
        return super().form_valid(form)


class ComponentListView(GroupRequiredMixin, ListView):
    group_required = "Vendors"
    model = BikeComponent
    template_name = 'component_list.html'
    context_object_name = 'componenti'
    paginate_by = 6

    def get_queryset(self):
        user_id = self.request.user.pk
        return BikeComponent.objects.filter(vendor=user_id)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Filtrare i componenti per ogni categoria e aggiungerli come variabili di contesto
        context['telaio'] = BikeComponent.objects.filter(category='Telaio', vendor=self.request.user.pk)
        context['manubrio'] = BikeComponent.objects.filter(category='Manubrio', vendor=self.request.user.pk)
        context['freno'] = BikeComponent.objects.filter(category='Freno', vendor=self.request.user.pk)
        context['sellino'] = BikeComponent.objects.filter(category='Sellino', vendor=self.request.user.pk)
        context['copertoni'] = BikeComponent.objects.filter(category='Copertoni', vendor=self.request.user.pk)

        return context


class ComponentUpdateView(GroupRequiredMixin, UpdateView):
    group_required = "Vendors"
    model = BikeComponent
    fields = ['category', 'name', 'price']
    template_name = 'component_update.html'
    success_url = reverse_lazy('Vendi:list_components')

    def form_valid(self, form):
        return super().form_valid(form)


@require_POST
def delete_component(request, pk):
    component = get_object_or_404(BikeComponent, pk=pk)
    if not BikeComponent.objects.contains(component):
        return HttpResponse(status=407, content='Errore')
    component.delete()
    return HttpResponse(status=207)