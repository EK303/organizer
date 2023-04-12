from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from users.models import TrelloUser
from main.models import Board

from .projects import ProjectTest


def get_user(username):
    return TrelloUser.objects.get(username=username)

class BoardTest(APITestCase):

    def setUp(self):
        testUser = TrelloUser(first_name="Joe", last_name="Joe", username="Rene",
                              password="Zeon1234", email="joe@zeon.com")
        testUser.is_active = True
        self.client.force_authenticate(user=testUser)
        testUser.save()

    def create_board(self):
        project = ProjectTest.create_project(self)
        board = Board(title="Board 123", project=project)
        board.save()
        return board

    def test_board_list_get(self):
        project_id = ProjectTest.create_project(self).id
        response = self.client.get(reverse("boards_main", kwargs={"project_id": project_id}),
                                   format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_board_create(self):
        project_id = ProjectTest.create_project(self).id
        response = self.client.post(reverse("boards_main", kwargs={"project_id": project_id}),
                                    {'title': 'Board 123', 'image': "", 'project_id': project_id},
                                    )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_board_view(self):
        board = self.create_board()
        response = self.client.get(reverse("board_detail", kwargs={"board_id": board.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_board_update(self):
        board = self.create_board()
        response = self.client.put(reverse("board_detail", kwargs={"board_id": board.id}), {'title': "Board 7856"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_board_delete(self):
        board = self.create_board()
        response = self.client.delete(reverse("board_detail", kwargs={"board_id": board.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_board_archive(self):
        board = self.create_board()
        response = self.client.post(reverse("boards_archive", kwargs={"project_id": board.project.id}),
                                    {"title": board.title,
                                     "archived": "True",
                                     "project_id": board.project.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_board_archived_view(self):
        project = ProjectTest.create_project(self)
        response = self.client.get(reverse("boards_archive", kwargs={"project_id": project.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_board_favour(self):
        board = self.create_board()
        response = self.client.post(reverse("boards_favour", kwargs={"project_id": board.project.id}),
                                    {"id": board.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_board_favour_view(self):
        project = ProjectTest.create_project(self)
        response = self.client.get(reverse("boards_favour", kwargs={"project_id": project.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


