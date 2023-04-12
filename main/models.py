from django.db import models

from users.models import TrelloUser


class Project(models.Model):
    title = models.CharField(max_length=30, unique=True)
    creator = models.ForeignKey(TrelloUser, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}"


class Board(models.Model):
    title = models.CharField(max_length=30)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="boards")
    archived = models.BooleanField(default=False)
    image = models.ImageField(default=None, blank=True, null=True)


class Membership(models.Model):
    member = models.ForeignKey(TrelloUser, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)


class Favourite(models.Model):
    person = models.ForeignKey(TrelloUser, on_delete=models.CASCADE)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)


class Column(models.Model):
    title = models.CharField(max_length=30)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="columns")


class Card(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(blank=True)
    column = models.ForeignKey(Column, on_delete=models.CASCADE, related_name="cards")
    due_date = models.DateField(null=True, blank=True, default=None)
    checklist = models.JSONField(default=dict, blank=True, null=True)

    class Meta:
        unique_together = ['title', 'column']


class File(models.Model):
    file = models.FileField(default=None, blank=True)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)


class Comment(models.Model):
    body = models.TextField(max_length=300)
    author = models.ForeignKey(TrelloUser, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE, related_name="comments")
    created_on = models.DateTimeField(auto_now_add=True)


class Mark(models.Model):
    title = models.CharField(max_length=30, unique=True)
    colour = models.CharField(max_length=30)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name="marks")

    class Meta:
        unique_together = ['title', 'board']


class MarkCard(models.Model):
    mark = models.ForeignKey(Mark, on_delete=models.CASCADE)
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
