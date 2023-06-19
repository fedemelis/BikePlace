from braces.views import *
from django.shortcuts import render
from django.utils import timezone
from django.views.generic import *

from Acquista.models import *

class HomeAcquistiView(LoginRequiredMixin, TemplateView):
    template_name = "home_acquisti.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        first_three_bike = Bike.objects.order_by('id')[:3]
        other_bike = Bike.objects.order_by('id')[3:]

        context['first_three_bike'] = first_three_bike
        context['other_bike'] = other_bike

        return context


class BikeListView(ListView):
    model = Bike
    template_name = "listabike.html"
    context_object_name = "bici_list"


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


"""TODO: Implementare la vista per la creazione di una bici"""
# class BikeCreateView(LoginRequiredMixin, CreateView):
#     model = Bike
#     # form_class = BikeForm
#     template_name = "bike_create.html"
#     # success_url = reverse_lazy("bike_list")
#
#     def form_valid(self, form):
#         form.instance.vendor = self.request.user
#         return super().form_valid(form)

