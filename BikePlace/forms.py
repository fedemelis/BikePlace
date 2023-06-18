from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from django import forms


class UsersForm(UserCreationForm):
    def save(self, commit=True):
        user = super().save(commit)
        g = Group.objects.get(name="Users")
        g.user_set.add(user)
        return user


class VendorsForm(UserCreationForm):
    def save(self, commit=True):
        user = super().save(commit)
        g = Group.objects.get(name="Vendors")
        g.user_set.add(user)
        return user
