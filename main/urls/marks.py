from django.urls import path

from main.views.marks import MarkDetailView

urlpatterns = [
    path("mark/<int:mark_id>", MarkDetailView.as_view(), name="mark_detail"),
]