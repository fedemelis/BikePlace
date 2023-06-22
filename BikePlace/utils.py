import pandas as pd
from django.contrib.auth.models import User
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
                matrix.loc[user, category] = 1


    print(matrix)

    return matrix

