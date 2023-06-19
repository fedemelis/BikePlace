from braces.views import *
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import *

from BikePlace.forms import *
from BikePlace.models import *



def WelcomePageView(request):
    return render(request, template_name='welcome.html')


class UserCreateView(CreateView):
    model = GenericUser
    form_class = UserForm
    template_name = "user_create.html"
    success_url = reverse_lazy("login")

class VendorCreateView(CreateView):
    model = GenericUser
    form_class = VendorForm
    template_name = "user_create.html"
    success_url = reverse_lazy("login")

class UserDetailView(LoginRequiredMixin, DetailView):
    model = GenericUser
    template_name = "user.html"
    context_object_name = "user"

    def get_object(self, queryset=None):
        return self.request.user


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = GenericUser
    form_class = UpdateUserForm
    template_name = "user_update.html"
    success_url = reverse_lazy("welcome_page")

    def get_object(self, queryset=None):
        return self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        login(self.request, self.object)  # Reimposta la sessione utente
        return response



