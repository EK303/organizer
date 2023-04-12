from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import TrelloUser

# Create your tests here.

class TrelloUserTest(APITestCase):

    def setUp(self):
        user = TrelloUser(first_name="user2", last_name="user2", username="user2",
                              password="Zeon1234", email="user2@zeon.com")
        user.save()

    def create_user(self):
        testUser = TrelloUser(first_name="Joe", last_name="Joe", username="Rene",
                              password="Zeon1234", email="joe@zeon.com")
        testUser.save()
        return testUser
    def test_registration(self):
        response = self.client.post(reverse("register"), {"first_name": "",
                                                              "last_name": "",
                                                              "username": "Username1",
                                                              "email": "good@day.com",
                                                              "password1": "Zeon1234",
                                                              "password2": "Zeon1234"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_account_activation(self):
        user = self.create_user()
        response = self.client.post(reverse("activate"), {"username": user.username,
                                                          "activation_code": user.activation_code})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(user.is_active, True)

    def test_login(self):
        response = self.client.post(reverse("login"), {"username": "user2",
                                                       "password": "Zeon1234"})
        print(response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

