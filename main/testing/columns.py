from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from users.models import TrelloUser
from main.models import Column

from .boards import BoardTest


def get_user(username):
    return TrelloUser.objects.get(username=username)


class ColumnTest(APITestCase):

    def setUp(self):
        testUser = TrelloUser(first_name="Joe", last_name="Joe", username="Rene",
                              password="Zeon1234", email="joe@zeon.com")
        testUser.is_active = True
        self.client.force_authenticate(user=testUser)
        testUser.save()

    def create_column(self):
        board = BoardTest.create_board(self)
        column = Column(title="Column 845", board=board)
        column.save()
        return column

    def test_column_create(self):
        board = BoardTest.create_board(self)
        response = self.client.post(reverse("column_main", kwargs={"board_id": board.id}), {"title": "Column 631",
                                                                                            "board_id": board.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_column_view(self):
        column = self.create_column()
        response = self.client.get(reverse("column_detail", kwargs={"column_id": column.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_column_update(self):
        column = self.create_column()
        response = self.client.put(reverse("column_detail", kwargs={"column_id": column.id}), {"title": "Column 8912",
                                                                                               "board_id": column.board.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_column_delete(self):
        column = self.create_column()
        response = self.client.delete(reverse("column_detail", kwargs={"column_id": column.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)