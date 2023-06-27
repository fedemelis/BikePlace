from django.db import transaction
from django.test import TestCase
from django.test.client import Client
from django.urls import reverse

from Acquista.models import Order, Bike, SoldBike, ShoppingCart, ShoppingCartItem
from BikePlace.models import GenericUser, Category, UserInterest
from django.contrib.auth.models import Group, User

from BikePlace.utils import build_matrix


class AcquistaViewTests(TestCase):


    client = Client()

    '''test per la view del carrello'''
    def test_missing_cart_items(self):
        response = self.client.get(reverse('Acquista:carrello', kwargs={'status': 'visit'}), follow=True)
        self.assertContains(response, 'Il carrello è vuoto!', status_code=200)


    def test_cart_items_present(self):
        self.create_shopping_cart()
        self.create_cart_item()
        response = self.client.get(reverse('Acquista:carrello', kwargs={'status': 'visit'}), follow=True)
        self.assertNotContains(response, 'Il carrello è vuoto!', status_code=200)


    '''test per la creazione delle raccomandazioni'''
    def test_building_recommendation(self):
        self.create_two_users()
        self.setup_categories()
        self.create_interests()
        result = build_matrix('u1')
        print(result)
        self.assertIn('category2', str(result))



    def create_interests(self):
        u1 = GenericUser.objects.get(username='u1')
        u2 = GenericUser.objects.get(username='u2')
        c1 = Category.objects.get(name='category1')
        c2 = Category.objects.get(name='category2')
        c3 = Category.objects.get(name='category3')

        u1_interest = UserInterest.objects.create(
            user=u1,
        )
        u1_interest.categories.add(c1)

        u2_interest = UserInterest.objects.create(
            user=u2,
        )
        u2_interest.categories.add(c1)
        u2_interest.categories.add(c2)

        u1_interest.save()
        u2_interest.save()

    def create_two_users(self):
        u1 = GenericUser.objects.create(
            username='u1',
            password='testpassword',
        )
        group = Group.objects.get(name='Users')
        u1.groups.add(group)

        u2 = GenericUser.objects.create(
            username='u2',
            password='testpassword',
        )
        u2.groups.add(group)


    def setup_categories(self):
        for i in range(1, 5):
            Category.objects.create(
                name=f'category{i}'
            )

    def create_vendor(self):
        return GenericUser.objects.create(
            username='testvendor',
            password='testpassword',
        )


    def create_bike(self):
        vendor = self.create_vendor()
        return SoldBike.objects.create(
            type_of_bike='test',
            brand='test',
            year_of_production=2023,
            price=100,
            vendor=vendor,
            image=None,
        )

    @transaction.atomic
    def create_shopping_cart(self):
         ShoppingCart.objects.get_or_create(
            user=GenericUser.objects.get(username='testuser'),
        )

    @transaction.atomic
    def create_cart_item(self):
        bike = self.create_bike()
        self.create_shopping_cart()
        shopCart = ShoppingCart.objects.get(user=GenericUser.objects.get(username='testuser'))
        ShoppingCartItem.objects.create(
            shopping_cart= shopCart,
            bike=bike,
        )


    def setUp(self) -> None:
        testUser = GenericUser.objects.create(
            username='testuser',
            password='testpassword',
        )
        group = Group.objects.create(name='Users')
        testUser.groups.add(group)



        self.client.force_login(testUser)


    def tearDown(self) -> None:
        GenericUser.objects.all().delete()
        SoldBike.objects.all().delete()
        ShoppingCart.objects.all().delete()
        ShoppingCartItem.objects.all().delete()
        Category.objects.all().delete()
        UserInterest.objects.all().delete()
