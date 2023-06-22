from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group, User
from django import forms

from BikePlace.models import *


class UserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        tipo_utente = kwargs.pop('tipo_utente', None)
        super().__init__(*args, **kwargs)

        if tipo_utente == 'azienda':
            self.fields['piva'] = forms.CharField(label='Partita IVA', max_length=11, required=True)


class Meta(UserCreationForm.Meta):
    model = GenericUser
    fields = UserCreationForm.Meta.fields + ('address', 'picture', 'piva')

    help_texts = {
        'piva': 'Inserisici la partita iva se sei un venditore',
    }


def save(self, commit=True):
    user = super().save(commit)
    if user.piva:
        g = Group.objects.get(name="Vendors")
        g.user_set.add(user)
    else:
        g = Group.objects.get(name="Users")
        g.user_set.add(user)
    return user


def verifica_partita_iva(self, partita_iva):
    partita_iva = partita_iva.strip()  # Rimuovi spazi bianchi

    if len(partita_iva) != 11:
        return False

    try:
        partita_iva = [int(digito) for digito in partita_iva]  # Converte in lista di interi
    except ValueError:
        return False

    # Calcola il controllo
    s = sum(partita_iva[i] if i % 2 == 0 else sum(divmod(partita_iva[i] * 2, 10)) for i in range(10))
    controllo = (10 - (s % 10)) % 10

    # Verifica che il controllo sia uguale all'ultimo cifra della partita IVA
    return controllo == partita_iva[10]


def clean_piva(self):
    piva = self.cleaned_data['piva']
    if piva is not None:
        if not self.verifica_partita_iva(piva):
            raise forms.ValidationError("Partita IVA non valida")
        else:
            return piva
    else:
        return piva


class UpdateUserForm(UserChangeForm):
    class Meta:
        model = GenericUser
        fields = ('first_name', 'last_name', 'username', 'email', 'address', 'picture', 'piva')


from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group, User
from django import forms

from BikePlace.models import *


class UserForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = GenericUser
        fields = UserCreationForm.Meta.fields + ('address', 'picture')

    def save(self, commit=True):
        user = super().save(commit)
        if user.piva:
            g = Group.objects.get(name="Vendors")
            g.user_set.add(user)
        else:
            g = Group.objects.get(name="Users")
            g.user_set.add(user)
        return user


class VendorForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = GenericUser
        fields = UserCreationForm.Meta.fields + ('address', 'picture', 'piva')


    def save(self, commit=True):
        user = super().save(commit)
        if user.piva:
            g = Group.objects.get(name="Vendors")
            g.user_set.add(user)
        else:
            g = Group.objects.get(name="Users")
            g.user_set.add(user)
        return user


    def verifica_partita_iva(self, partita_iva):
        partita_iva = partita_iva.strip()  # Rimuovi spazi bianchi

        if len(partita_iva) != 11:
            return False

        try:
            partita_iva = [int(digito) for digito in partita_iva]  # Converte in lista di interi
        except ValueError:
            return False

        # Calcola il controllo
        s = sum(partita_iva[i] if i % 2 == 0 else sum(divmod(partita_iva[i] * 2, 10)) for i in range(10))
        controllo = (10 - (s % 10)) % 10

        # Verifica che il controllo sia uguale all'ultimo cifra della partita IVA
        return controllo == partita_iva[10]


    def clean_piva(self):
        piva = self.cleaned_data['piva']
        if piva is not None:
            if not self.verifica_partita_iva(piva):
                raise forms.ValidationError("Partita IVA non valida")
            else:
                return piva
        else:
            return piva


class UpdateUserForm(UserChangeForm):
    class Meta:
        model = GenericUser
        fields = ('first_name', 'last_name', 'username', 'email', 'address', 'picture', 'piva')


class UserInterestForm(forms.ModelForm):
    class Meta:
        model = UserInterest
        fields = ['categories']

    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'})
    )

