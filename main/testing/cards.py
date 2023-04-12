from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from users.models import TrelloUser
from main.models import Card, Project, Board, Mark

from .boards import BoardTest
from .columns import ColumnTest


def get_user(username):
    return TrelloUser.objects.get(username=username)


class CardTest(APITestCase):

    def setUp(self):
        testUser = TrelloUser(first_name="Joe", last_name="Joe", username="Rene",
                              password="Zeon1234", email="joe@zeon.com")
        testUser.is_active = True
        self.client.force_authenticate(user=testUser)
        testUser.save()

    def create_card(self):
        column = ColumnTest.create_column(self)
        card = Card(title="Card 123", description="Some good card", column=column)
        card.save()
        return card

    def create_mark(self):
        board = BoardTest.create_board(self)
        mark = Mark(title="Mark 1234", colour="#2696be", board=board)
        mark.save()
        return mark

    def test_card_create(self):
        column = ColumnTest.create_column(self)
        response = self.client.post(reverse("card_main", kwargs={"column_id": column.id}), {"title": "Card 125",
                                                                                            "description": "Great day",
                                                                                            "due_date": "",
                                                                                            "column_id": column.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_card_view(self):
        card = self.create_card()
        response = self.client.get(reverse("card_detail", kwargs={"card_id": card.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_card_update(self):
        card = self.create_card()
        response = self.client.put(reverse("card_detail", kwargs={"card_id": card.id}),
                                   {"title": "Card 5428",
                                    "description": "Updated card",
                                    "due_date": "2023-01-01",
                                    "checklist": "",
                                    "column_id": card.column.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_card_delete(self):
        card = self.create_card()
        response = self.client.delete(reverse("card_detail", kwargs={"card_id": card.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_mark_create(self):
        board = BoardTest.create_board(self)
        response = self.client.post(reverse("marks_main", kwargs={"board_id": board.id}),
                                    {"title": "Mark 123",
                                     "colour": "#2596be",
                                     "board_id": board.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_mark_view(self):
        mark = self.create_mark()
        response = self.client.get(reverse("mark_detail", kwargs={"mark_id": mark.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_mark_update(self):
        mark = self.create_mark()
        user = get_user("Rene")
        project = Project(title="Project 987", creator=user)
        project.save()
        board = Board(title="Board 987", project=project)
        board.save()
        response = self.client.put(reverse("mark_detail", kwargs={"mark_id": mark.id}),
                                   {"title": "New Mark",
                                    "colour": "#1296be",
                                    "board_id": board.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)\

    def test_mark_delete(self):
        mark = self.create_mark()
        response = self.client.delete(reverse("mark_detail", kwargs={"mark_id": mark.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
