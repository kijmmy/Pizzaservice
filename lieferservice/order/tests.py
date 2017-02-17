from django.test import TestCase
from order.models import *

from decimal import Decimal

class ModelTestCase(TestCase):
    #this is bad conformation-bias-testing!
    def setUp(self):
        premeal = Meal.objects.create(
            name="Pizza",
            description="round!",
            recipie="Bake dough in oven."
        )
        meal = Price.objects.create(
            meal = premeal,
            value = 42.23,
            size = "X"
        )
        order = Order.objects.create(
            address="Waldlindengasse 42, Hintertupfingen"
        )
        Topping.objects.create(
            meal=meal,
            order = order,
            topping="HAM"
        )

    def test_meals_are_expensive(self):
        order = Order.objects.get()
        self.assertEqual(order.state, 'R')
        self.assertEqual(order.meals.get().value, Decimal("42.23"))
        self.assertEqual(order.meals.get().meal.name, "Pizza")

from django.contrib.auth.models import AnonymousUser, User, Permission
from django.core.exceptions import PermissionDenied
from django.test import RequestFactory, Client
from django.urls import reverse
from order.views import *

DEPLOY_ADDRES="https://www.pizza.boringurl"

class RequestTests(TestCase):
    def setUp(self):
        COOK = (
            Permission.objects.get(codename='view_recipie'),
            Permission.objects.get(codename='change_state'),
        )
        self.client = Client()

        meal = Meal.objects.create(
            name="Great Mykonos",
            recipie="warm up frozen stuff and sell for 10€",
            description="Delightfully handmade sculpture of Alexander the great out of delicious ingredients!"
        )
        self.meal = Price.objects.create(meal=meal, value=42, size="LARGE")
        self.factory = RequestFactory()
        self.anon = AnonymousUser()
        self.visitor = User.objects.create_user(
            username='john',
            password='doe',
            email='john@dough.ugh'
        )
        self.cook = User.objects.create_user(
            username='gaston',
            password='pardonmyfrench',
            email='such@good.boy'
        )
        self.cook.user_permissions.set(COOK)

    def test_menu(self):
        view = ListMenu.as_view()
        request = self.factory.get('/', HTTP_HOST=DEPLOY_ADDRES)
        request.user = self.anon
        response1 = view(request)
        request.user = self.visitor
        response2 = view(request)
        request.user = self.cook
        response3 = view(request)

        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response3.status_code, 200)

    def test_cant_see_recipie(self):
        view = ShowMeal.as_view()
        request = self.factory.get('/order/', HTTP_HOST=DEPLOY_ADDRES)
        request.user = self.anon
        response1 = view(request, slug=self.meal.pk)
        request.user = self.visitor
        response2 = view(request, slug=self.meal.pk)
        request.user = self.cook
        response3 = view(request, slug=self.meal.pk)

        self.assertEqual(response1.status_code, 200)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response3.status_code, 200)

    def test_order(self):
        view = OrderMeal.as_view()
        request = self.factory.get('/order/', HTTP_HOST=DEPLOY_ADDRES)
        request.user = self.anon
        response1 = view(request)
        request.user = self.visitor
        response2 = view(request)
        request.user = self.cook
        response3 = view(request)

        #assert redirect
        self.assertEqual(response1.status_code, 302)
        self.assertEqual(response2.status_code, 200)
        self.assertEqual(response3.status_code, 200)

    def test_change_status(self):
        view = ChangeOrderState.as_view()
        order = Order.objects.create(address="somefuckingstring")
        Topping.objects.create(meal=self.meal, order=order, topping='MUSHROOMS')
        request = self.factory.get('/order/', {'state':'BAKING'}, HTTP_HOST=DEPLOY_ADDRES)
        request.user = self.anon
        with self.assertRaises(PermissionDenied):
            view(request, slug=order.pk)
        request.user = self.visitor
        with self.assertRaises(PermissionDenied):
            view(request, slug=order.pk)

        request.user = self.cook
        response = view(request, slug=self.meal.pk)
        self.assertEqual(response.status_code, 200)