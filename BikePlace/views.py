from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView

from BikePlace.forms import *


def WelcomePageView(request):
    return render(request, template_name='welcome.html')


class UserCreateView(CreateView):
    form_class = UsersForm
    template_name = "user_create.html"
    success_url = reverse_lazy("login")


class VendorCreateView(CreateView):
    form_class = VendorsForm
    template_name = "user_create.html"
    success_url = reverse_lazy("login")
