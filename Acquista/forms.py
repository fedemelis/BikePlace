from django import forms

from Acquista.models import CompositeBike, BikeComponent


class CompositeBikeForm(forms.ModelForm):
    class Meta:
        model = CompositeBike
        fields = ['telaio', 'manubrio', 'freno', 'sellino', 'copertoni']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['telaio'].queryset = BikeComponent.objects.filter(category='Telaio')
        self.fields['manubrio'].queryset = BikeComponent.objects.filter(category='Manubrio')
        self.fields['freno'].queryset = BikeComponent.objects.filter(category='Freno')
        self.fields['sellino'].queryset = BikeComponent.objects.filter(category='Sellino')
        self.fields['copertoni'].queryset = BikeComponent.objects.filter(category='Copertoni')
