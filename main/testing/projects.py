from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse

from users.models import TrelloUser
from main.models import Project


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

