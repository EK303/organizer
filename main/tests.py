from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from users.models import TrelloUser
from main.models import Project, Board, Column, Card, Mark


def get_user(username):
    return TrelloUser.objects.get(username=username)


class ProjectTest(APITestCase):

    def setUp(self):
        testUser = TrelloUser(first_name="Joe", last_name="Joe", username="Rene",
                              password="Zeon1234", email="joe@zeon.com")
        testUser.is_active = True
        self.client.force_authenticate(user=testUser)
        testUser.save()

    def create_project(self):
        user = get_user("Rene")
        project = Project(title="Project 123", creator=user)
        project.save()
        return project

    def create_board(self):
        project = self.create_project()
        board = Board(title="Board 123", project=project)
        board.save()
        return board

    def create_column(self):
        board = self.create_board()
        column = Column(title="Column 845", board=board)
        column.save()
        return column

    def create_card(self):
        column = self.create_column()
        card = Card(title="Card 123", description="Some good card", column=column)
        card.save()
        return card

    def create_mark(self):
        board = self.create_board()
        mark = Mark(title="Mark 1234", colour="#2696be", board=board)
        mark.save()
        return mark

    def test_project_get(self):
        response = self.client.get(reverse('projects_main'), format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_project_create(self):
        user = TrelloUser.objects.get(username="Rene")
        response = self.client.post(reverse('projects_main'), {'title': 'Project 124',
                                                               'creator_username': user.username}, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_project_detail(self):
        response = self.client.get(reverse('project_details', kwargs={"project_id": self.create_project().id}),
                                   format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_board_list_get(self):
        response = self.client.get(reverse("boards_main", kwargs={"project_id": self.create_project().id}),
                                   format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_board_create(self):
        project_id = self.create_project().id
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

    def test_column_create(self):
        board = self.create_board()
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

    def test_card_create(self):
        column = self.create_column()
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
        board = self.create_board()
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
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_mark_delete(self):
        mark = self.create_mark()
        response = self.client.delete(reverse("mark_detail", kwargs={"mark_id": mark.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_comment_create(self):
        card = self.create_card()
        response = self.client.post(reverse("comment_add", kwargs={"card_id": card.id}), {"body": "Hello"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_board_archive(self):
        board = self.create_board()
        response = self.client.post(reverse("boards_archive", kwargs={"project_id": board.project.id}),
                                    {"title": board.title,
                                     "archived": "True",
                                     "project_id": board.project.id})

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_board_archived_view(self):
        project = self.create_project()
        response = self.client.get(reverse("boards_archive", kwargs={"project_id": project.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_board_favour(self):
        board = self.create_board()
        response = self.client.post(reverse("boards_favour", kwargs={"project_id": board.project.id}),
                                    {"id": board.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_board_favour_view(self):
        project = self.create_project()
        response = self.client.get(reverse("boards_favour", kwargs={"project_id": project.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)