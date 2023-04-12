from django.urls import path

from main.views.cards import CardDetailView, CommentCreateView


urlpatterns = [
    path("card/<int:card_id>", CardDetailView.as_view(), name="card_detail"),
    path("card/<int:card_id>/comment", CommentCreateView.as_view(), name="comment_add"),
]