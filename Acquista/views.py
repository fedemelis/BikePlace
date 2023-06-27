import asyncio
import random
from itertools import islice

from braces.views import *
from django.contrib.auth import get_user_model
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.generic import *
from django.db.models import Q, Subquery

from Acquista.forms import CompositeBikeForm
from Acquista.models import *
from django.db.models import Sum

from BikePlace.models import UserInterest
from BikePlace.utils import build_matrix, sendMail


class HomeAcquistiView(GroupRequiredMixin, TemplateView):
    group_required = 'Users'
    template_name = "home_acquisti.html"

    def get(self, request, *args, **kwargs):
        # Controlla se esiste un oggetto UserInterest per l'utente corrente
        user_interest = UserInterest.objects.filter(user=self.request.user).first()

        if not user_interest:
            # Reindirizza l'utente a un'altra pagina con la pk come parametro
            return redirect('interessi', pk=self.request.user.pk)
        return super().get(request, *args, **kwargs)


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

        recommended_bike_dict = build_matrix()
        user_bikes = recommended_bike_dict.get(self.request.user.username, {})

        recommended1 = None
        recommended2 = None
        recommended3 = None

        if len(user_bikes) > 0:
            recommended1 = Bike.objects.exclude(
                Q(vendor=self.request.user) | Q(soldbike__isnull=False)
            ).filter(type_of_bike=user_bikes[0]).order_by('?').first()
        if len(user_bikes) > 1:
            recommended2 = Bike.objects.exclude(
                Q(vendor=self.request.user) | Q(soldbike__isnull=False)
            ).filter(type_of_bike=user_bikes[1]).order_by('?').first()
        if len(user_bikes) > 2:
            recommended3 = Bike.objects.exclude(
                Q(vendor=self.request.user) | Q(soldbike__isnull=False)
            ).filter(type_of_bike=user_bikes[2]).order_by('?').first()

        #prendo gli interessi dell'utente
        user_interest = UserInterest.objects.filter(user=self.request.user).first()

        # Seleziona casualmente una categoria dalle categorie dell'oggetto UserInterest
        category = random.choice(user_interest.categories.all())

        print(category)

        # Seleziona una bici casuale della categoria scelta
        discounted_bike = Bike.objects.exclude(
            Q(vendor=self.request.user) | Q(soldbike__isnull=False)
        ).filter(type_of_bike=category).order_by('?').first()

        existing_discount = BikeDiscount.objects.filter(user=self.request.user).first()

        if existing_discount:
            context['discounted_bike'] = existing_discount
            # Verifica se lo sconto è attivo da più di un giorno
            time_threshold = timezone.now() - timezone.timedelta(days=1)
            if existing_discount.start_date < time_threshold:
                # Aggiorna lo sconto con i nuovi valori
                existing_discount.bike = discounted_bike
                existing_discount.newPrice = discounted_bike.price * 0.5
                existing_discount.start_date = timezone.now()
                existing_discount.save()
                if self.request.user.email:
                    asyncio.run(sendMail(
                        "Nuovo sconto disponibile",
                        f"Ciao, è disponibile uno sconto per una {existing_discount.bike.type_of_bike} che potrebbe interessarti. Vai su BikePlace per maggiori informazioni.",
                        "fedemelis1@gmail.com",
                        [self.request.user.email]
                    ))
        else:
            # Crea un nuovo oggetto BikeDiscount
            if discounted_bike:
                bike_discount = BikeDiscount.objects.create(user=self.request.user, bike=discounted_bike,
                                                            newPrice=discounted_bike.price * 0.5,
                                                            start_date=timezone.now())
                if self.request.user.email:
                    asyncio.run(sendMail(
                        "Nuovo sconto disponibile",
                        f"Ciao, è disponibile uno sconto per una {bike_discount.bike.type_of_bike} che potrebbe interessarti. Vai su BikePlace per maggiori informazioni.",
                        "fedemelis1@gmail.com",
                        [self.request.user.email]
                    ))
                context['discounted_bike'] = bike_discount

        # print(recommended1, recommended2, recommended3)

        print(discounted_bike)

        if recommended1:
            context['recommended1'] = recommended1
        if recommended2:
            context['recommended2'] = recommended2
        if recommended3:
            context['recommended3'] = recommended3

        return context


class BikeListView(ListView):
    model = Bike
    template_name = "listabike.html"
    context_object_name = "bici_list"
    paginate_by = 6

    def get_queryset(self):
        # Ottieni una subquery per ottenere i sold_bike_id
        sold_bike_ids = SoldBike.objects.values('id')

        # Filtra le biciclette escludendo quelle che hanno l'id presente nella subquery
        queryset = Bike.objects.exclude(id__in=Subquery(sold_bike_ids))

        # Ottieni il parametro di ricerca dalla query string
        search_query = self.request.GET.get('q')

        if search_query:
            # Filtra le bici in base al parametro di ricerca
            queryset = queryset.filter(
                Q(type_of_bike__icontains=search_query) |
                Q(brand__icontains=search_query)
            )

        # Ottieni il parametro di ordinamento dalla query string
        sort_by = self.request.GET.get('sort')

        if sort_by == 'price_c':
            # Ordina le bici per prezzo in ordine crescente
            queryset = queryset.order_by('price')
        elif sort_by == 'price_d':
            # Ordina le bici per prezzo in ordine decrescente
            queryset = queryset.order_by('-price')
        elif sort_by == 'year_c':
            # Ordina le bici per anno di produzione in ordine crescente
            queryset = queryset.order_by('year_of_production')
        elif sort_by == 'year_d':
            # Ordina le bici per anno di produzione in ordine decrescente
            queryset = queryset.order_by('-year_of_production')

        queryset = queryset.exclude(compositebike__isnull=False)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Ottieni il valore del parametro 'q' dalla query string dell'URL
        search_query = self.request.GET.get('q')

        context['keyword_query'] = search_query

        return context


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        context['preferiti'] = FavoriteBike.objects.filter(user=user).values_list('bike__pk', flat=True)

        context['prev_page'] = self.request.META.get('HTTP_REFERER')

        if self.request.META.get('HTTP_REFERER') == "http://127.0.0.1:8000/acquista/homeacquisti/":
            context['prev_page'] = "http://127.0.0.1:8000/acquista/homeacquisti/"
        elif self.request.META.get('HTTP_REFERER') == "http://127.0.0.1:8000/acquista/listabici/":
            context['prev_page'] = "http://127.0.0.1:8000/acquista/listabici/"
        else:
            context['prev_page'] = ""

        return context


class ShoppingCartView(GroupRequiredMixin, ListView):
    group_required = "Users"
    model = ShoppingCartItem
    template_name = "shopping_cart_item_list.html"
    context_object_name = "cart_items"

    def get_queryset(self):
        user = self.request.user
        shopping_cart = ShoppingCart.objects.get(user=user)
        queryset = super().get_queryset().filter(shopping_cart=shopping_cart)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user
        context['carrello_utente'] = ShoppingCart.objects.get(user=user)

        return context


class AggiungiAlCarrelloView(GroupRequiredMixin, View):
    group_required = "Users"
    def get(self, request, pk):
        bici = Bike.objects.get(pk=pk)

        # Verifica se l'utente ha già un carrello, altrimenti crea uno nuovo
        try:
            carrello = ShoppingCart.objects.get(user=request.user)
        except ShoppingCart.DoesNotExist:
            carrello = ShoppingCart.objects.create(user=request.user)

        # Aggiungi la bici al carrello
        ShoppingCartItem.objects.get_or_create(shopping_cart=carrello, bike=bici)

        # Ridirigi l'utente alla pagina del carrello o a un'altra pagina desiderata
        return redirect('Acquista:home_acquisti')


class RimuoviDalCarrelloView(GroupRequiredMixin, View):
    group_required = "Users"
    def get(self, request, pk):
        bici = Bike.objects.get(pk=pk)

        # Verifica se l'utente ha già un carrello, altrimenti crea uno nuovo
        try:
            carrello = ShoppingCart.objects.get(user=request.user)
        except ShoppingCart.DoesNotExist:
            carrello = ShoppingCart.objects.create(user=request.user)

        # Rimuovi la bici dal carrello
        ShoppingCartItem.objects.filter(shopping_cart=carrello, bike=bici).delete()

        # Ridirigi l'utente alla pagina del carrello
        return redirect('Acquista:carrello', status="removed")


@require_POST
def flush_shopping_cart(request, pk):
    shopping_cart = get_object_or_404(ShoppingCart, pk=pk)

    # Verifica se il carrello appartiene all'utente corrente
    if not ShoppingCart.objects.filter(user=request.user, pk=pk).exists():
        return HttpResponse(status=407, content='Errore')

    # Rimuovi tutti gli elementi di ShoppingCartItem associati al carrello
    ShoppingCartItem.objects.filter(shopping_cart=shopping_cart).delete()

    return HttpResponse(status=207)


class OrderConfirmationView(GroupRequiredMixin, View):
    group_required = 'Users'
    def get(self, request, pk):
        shopping_cart = get_object_or_404(ShoppingCart, pk=pk)

        # Verifica se il carrello appartiene all'utente corrente
        if not ShoppingCart.objects.filter(user=request.user, pk=pk).exists():
            return HttpResponse(status=407, content='Errore')

        total = 0

        # Crea un nuovo ordine
        order = Order.objects.create(user=request.user, total_price=total)

        # Itera sugli elementi del carrello
        for item in ShoppingCartItem.objects.filter(shopping_cart=shopping_cart):
            print(item)
            seller, created = Seller.objects.get_or_create(
                username=item.bike.vendor.username + '_seller' + str(item.bike.vendor.id))

            # Crea un'istanza di SoldBike per ogni elemento del carrello
            sold_bike = SoldBike.objects.create(
                type_of_bike=item.bike.type_of_bike,
                year_of_production=item.bike.year_of_production,
                brand=item.bike.brand,
                price=item.bike.price,
                vendor=seller
                # Altri campi della bici da impostare
            )

            total += item.bike.price

            if not item.bike.brand == "Creata da me":
                Bike.objects.filter(pk=item.bike.pk).delete()

            # Aggiungi l'istanza di SoldBike all'ordine
            order.sold_bikes.add(sold_bike)

        print(total)

        order.total_price = total

        order.save()
        total = 0

        # Rimuovi tutti gli elementi di ShoppingCartItem associati al carrello
        ShoppingCartItem.objects.filter(shopping_cart=shopping_cart).delete()

        return redirect('Acquista:carrello', status="confirmed")


class OrderListView(GroupRequiredMixin, ListView):
    group_required = 'Users'
    model = Order
    template_name = "order_list.html"
    context_object_name = "order_list"
    paginate_by = 3

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-order_date')


class AggiungiPreferitoView(GroupRequiredMixin, View):
    group_required = 'Users'

    def get(self, request, pk):
        bici = Bike.objects.get(pk=pk)
        user = request.user

        favBike = FavoriteBike.objects.create(user=user, bike=bici)

        favBike.save()

        redirect_url = reverse('Acquista:dettagliobici', kwargs={'pk': pk})
        query_params = request.GET.urlencode()

        if query_params:
            redirect_url += '?' + query_params

        return redirect(redirect_url)


class RimuoviPreferitoView(GroupRequiredMixin, View):
    group_required = 'Users'

    def get(self, request, pk):
        bici = Bike.objects.get(pk=pk)
        user = request.user

        FavoriteBike.objects.filter(user=user, bike=bici).delete()

        redirect_url = reverse('Acquista:dettagliobici', kwargs={'pk': pk})
        query_params = request.GET.urlencode()

        if query_params:
            redirect_url += '?' + query_params

        return redirect(redirect_url)



class RimuoviPreferitoFromList(GroupRequiredMixin, View):
    group_required = 'Users'

    def get(self, request, pk):
        bici = Bike.objects.get(pk=pk)
        user = request.user

        FavoriteBike.objects.filter(user=user, bike=bici).delete()

        return redirect('Acquista:listapreferiti', pk=pk)


class FavoriteBikeListView(GroupRequiredMixin, ListView):
    group_required = 'Users'
    model = FavoriteBike
    template_name = "favorite_bike_list.html"
    context_object_name = "favorite_bike_list"

    def get_queryset(self):
        user = self.request.user
        favBike = FavoriteBike.objects.filter(user=user).values_list('bike__pk', flat=True)
        return Bike.objects.filter(pk__in=favBike)


class CreateCompositeBikeView(GroupRequiredMixin, CreateView):
    group_required = 'Users'
    model = CompositeBike
    form_class = CompositeBikeForm
    template_name = "create_composite_bike.html"
    success_url = reverse_lazy('Acquista:home_acquisti')

    def form_valid(self, form):
        form.instance.vendor = self.request.user
        # Salva la bici composta
        response = super().form_valid(form)

        # Aggiungi la bici composta al carrello
        carrello = self.get_shopping_cart()
        ShoppingCartItem.objects.create(shopping_cart=carrello, bike=self.object)

        return response

    def get_shopping_cart(self):
        # Verifica se l'utente ha già un carrello, altrimenti crea uno nuovo
        try:
            carrello = ShoppingCart.objects.get(user=self.request.user)
        except ShoppingCart.DoesNotExist:
            carrello = ShoppingCart.objects.create(user=self.request.user)
        return carrello






