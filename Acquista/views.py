from itertools import islice

from braces.views import *
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import *
from django.db.models import Q
from Acquista.models import *


class HomeAcquistiView(LoginRequiredMixin, TemplateView):
    template_name = "home_acquisti.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)


        bike_views = BikeViewed.objects.filter(
            Q(user=self.request.user) & ~Q(bike__vendor=self.request.user)
        ).order_by('-viewed_at')

        first_three_bike_id = list(bike_views.values_list('bike', flat=True)[:3])
        other_bike_id = list(bike_views.values_list('bike', flat=True)[3:6])

        first_three_bike = [get_object_or_404(Bike, id=bike_id) for bike_id in first_three_bike_id]
        other_bike = [get_object_or_404(Bike, id=bike_id) for bike_id in other_bike_id]

        context['first_three_bike'] = first_three_bike
        context['other_bike'] = other_bike

        return context


class BikeListView(ListView):
    model = Bike
    template_name = "listabike.html"
    context_object_name = "bici_list"
    paginate_by = 6


class BikeDetailView(LoginRequiredMixin, DetailView):
    model = Bike
    template_name = "bikedetail.html"
    context_object_name = "bici"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()

        # Aggiorna la data di visualizzazione se l'oggetto BikeViewed esiste già
        if request.user.is_authenticated:
            viewed_obj, created = BikeViewed.objects.get_or_create(user=request.user, bike=self.object)
            if not created:
                viewed_obj.viewed_at = timezone.now()
                viewed_obj.save()

        return self.render_to_response(self.get_context_data())


class ShoppingCartView(LoginRequiredMixin, ListView):
    model = ShoppingCartItem
    template_name = "shoppin_cart_item_list.html"
    context_object_name = "cart_items"

    def get_queryset(self):
        user = self.request.user
        shopping_cart = ShoppingCart.objects.get(user=user)
        queryset = super().get_queryset().filter(shopping_cart=shopping_cart)
        return queryset


class AggiungiAlCarrelloView(LoginRequiredMixin, View):
    def get(self, request, pk):
        bici = Bike.objects.get(pk=pk)

        # Verifica se l'utente ha già un carrello, altrimenti crea uno nuovo
        try:
            carrello = ShoppingCart.objects.get(user=request.user)
        except ShoppingCart.DoesNotExist:
            carrello = ShoppingCart.objects.create(user=request.user)

        # Aggiungi la bici al carrello
        ShoppingCartItem.objects.create(shopping_cart=carrello, bike=bici)

        # Ridirigi l'utente alla pagina del carrello o a un'altra pagina desiderata
        return redirect('Acquista:dettagliobici', pk=pk)
