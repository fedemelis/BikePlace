from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, User
from django import forms

from BikePlace.models import *


class UserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = GenericUser
        fields = UserCreationForm.Meta.fields + ("address", "picture", "piva")

    def save(self, commit=True):
        user = super().save(commit)
        if user.piva:
            g = Group.objects.get(name="Vendors")
            g.user_set.add(user)
        else:
            g = Group.objects.get(name="Users")
            g.user_set.add(user)
        return user
