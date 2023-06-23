import pandas as pd
from django.contrib.auth.models import User

from Acquista.models import CompositeBike, BikeComponent
from .models import UserInterest, GenericUser, Category


def build_matrix():
    # Ottenere tutti gli utenti che fanno parte del gruppo "Users"
    users = GenericUser.objects.filter(groups__name='Users')

    # Ottenere tutti gli interessi degli utenti
    interests = UserInterest.objects.all()

    categories = Category.objects.values_list('name', flat=True)

    # Creare la matrice vuota con le dimensioni corrette
    matrix = pd.DataFrame(index=users, columns=categories, dtype=int)

    # Riempire la matrice con i dati degli interessi degli utenti
    for user in users:
        user_interests = interests.filter(user=user)
        for interest in user_interests:
            for category in interest.categories.all():
                category_name = category.name  # Ottenere il nome della categoria
                matrix.loc[user, category_name] = 1

    print(matrix)

    return matrix


def test():
    telaio = BikeComponent.objects.get_or_create(name='Telaio', category='Telaio', price=200)
    manubrio = BikeComponent.objects.get_or_create(name='Manubrio', category='Manubrio', price=50)
    freno = BikeComponent.objects.get_or_create(name='Freno', category='Freno', price=100)
    sellino = BikeComponent.objects.get_or_create(name='Sellino', category='Sellino', price=80)
    copertoni = BikeComponent.objects.get_or_create(name='Copertoni', category='Copertoni', price=120)

    vendor = GenericUser.objects.get(username='admin')

    # Creazione di una CompositeBike
    composite_bike = CompositeBike(
        telaio=telaio,
        manubrio=manubrio,
        freno=freno,
        sellino=sellino,
        copertoni=copertoni,
        vendor=vendor,
        image='bici_composta.jpg'
    )
    composite_bike.save()

