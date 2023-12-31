import pandas as pd
from django.contrib.auth.models import User
from django.core.mail import send_mail
from sklearn.metrics.pairwise import cosine_similarity

from Acquista.models import CompositeBike, BikeComponent
from .models import UserInterest, GenericUser, Category


def build_matrix(selectedUser=None):
    # ottengo tutti gli utenti che fanno parte del gruppo "Users"
    users = GenericUser.objects.filter(groups__name='Users')

    # ottengo tutti gli interessi degli utenti
    interests = UserInterest.objects.all()

    categories = Category.objects.values_list('name', flat=True)

    # creo la matrice vuota con le dimensioni corrette
    matrix = pd.DataFrame(index=users, columns=categories, dtype=int)
    matrix = matrix.fillna(0)  # riempio la matrice con 0

    # riempio la matrice con i dati degli interessi degli utenti
    for user in users:
        user_interests = interests.filter(user=user)
        for interest in user_interests:
            for category in interest.categories.all():
                category_name = category.name
                matrix.loc[user, category_name] = 1

    similarity_scores = cosine_similarity(matrix)

    similarity_matrix = pd.DataFrame(similarity_scores, index=users, columns=users)

    user_recommendations = {}
    for user in users:
        userObj = GenericUser.objects.get(username=user)
        recommended_categories = get_category_recommendations(similarity_matrix, matrix, userObj, max_recommendations=3)
        user_recommendations[user.username] = recommended_categories

    if selectedUser is not None:
        return user_recommendations.get(selectedUser)
    else:
        return user_recommendations


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


''' 
viene fornita la matrice di similarità fra gli utenti che abbiamo calcolato sopra con la similarità coseno
viene passata matrix che è la matrice degli interessi degli utenti
viene passato l'utente per cui dobbiamo fare le raccomandazioni
viene passato il numero massimo di raccomandazioni da fare     
'''


def get_category_recommendations(similarity_matrix, matrix, user, max_recommendations=3):
    similar_users = similarity_matrix.loc[user].drop(user).sort_values(ascending=False)

    # Trovare le categorie di bici che interessano agli utenti più simili, escludendo quelle già presenti per l'utente corrente
    recommended_categories = {}
    for similar_user in similar_users.index:
        # seleziono le categorie di bici che interessano all'utente simile
        similar_user_categories = set(matrix.loc[similar_user][matrix.loc[similar_user] == 1].index)
        user_categories = set(matrix.loc[user][matrix.loc[user] == 1].index)
        # prendo le categorie che interessano all'utente simile ma non all'utente corrente
        new_categories = similar_user_categories - user_categories
        # qua conto per ogni categoria quante volte è stata raccomandata
        for category in new_categories:
            if category in recommended_categories:
                recommended_categories[category] += 1
            else:
                recommended_categories[category] = 1

    # ordino le categorie raccomandate in ordine decrescente di raccomandazioni
    recommended_categories = sorted(recommended_categories.items(), key=lambda x: x[1], reverse=True)

    recommended_categories = [category for category, _ in recommended_categories][:max_recommendations]

    return recommended_categories


async def sendMail(oggetto, body, sender, reciver):
    send_mail(
        oggetto,  # oggetto del messaggio
        body,  # contenuto del messaggio
        sender,  # indirizzo email di invio
        reciver,  # lista degli indirizzi email di destinazione
        fail_silently=True,  # solleva un'eccezione in caso di errore
    )
